"""
This shows one way to ensure isolation between tests by creating a temporary table
that is only available for the duration of the database connection.
"""
import pytest
import psycopg2


class TestDatabase:
    def __init__(self, host="localhost", port=5432, name="postgres"):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=name,
        )

    def setup(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE TEMPORARY TABLE test_users_table (name VARCHAR(255));"
                )

    def teardown(self):
        self.conn.close()


class CreateUserAction:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, db: TestDatabase):
        with db.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO test_users_table (name) VALUES ('{self.name}');"
                )


@pytest.fixture(scope="module")
def db():
    db = TestDatabase()
    db.setup()
    yield db
    db.teardown()


def test_create_user_action(db):
    with db.conn as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM test_users_table;")
            count_before_adding_users = cur.fetchone()[0]

    CreateUserAction(name="Alice")(db)

    with db.conn as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM test_users_table;")
            count_after_adding_users = cur.fetchone()[0]

    assert count_after_adding_users == count_before_adding_users + 1

if __name__ == "__main__":
    from concurrent.futures import ProcessPoolExecutor

    num_concurrent_processes = 4
    with ProcessPoolExecutor(max_workers=10) as executor:
        outputs = [
            executor.submit(
                pytest.main,
                [__file__],
                plugins=[],
            )
            for _ in range(num_concurrent_processes)
        ]

    passed = 0
    for i, out in enumerate(outputs, start=1):
        if out.result() == pytest.ExitCode.OK:
            passed += 1

    print(f"{passed}/{num_concurrent_processes} passed")
