"""
This is a flaky test. It fails due to improper isolation between tests. The
problem is that the same test table could be modified by different tests or
concurrent test runs.
"""
# ----------------------------------
# Implementation - create_user.py
# ----------------------------------
import pytest

class CreateUserAction:
    def __init__(self, name):
        self.name = name

    def run(self, db):
        with db.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO test_users_table (name) VALUES ('{self.name}');"
                )

# ----------------------------------
# test suite - conftest.py
# ----------------------------------
import os
import psycopg2

class TestDatabase:
    def __init__(self, db_url=None):
        if db_url is None:
            db_url = os.environ["TEST_DATABASE__URL"]
        self.conn = psycopg2.connect(db_url)

    def setup(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS test_users_table (name VARCHAR(255));"
                )

    def teardown(self):
        self.conn.close()


@pytest.fixture(scope="session")
def db():
    db = TestDatabase()
    db.setup()
    yield db
    db.teardown()


# ----------------------------------
# test suite - test_create_user.py
# ----------------------------------

def test_create_user_action(db):
    with db.conn as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM test_users_table;")
            count_before_adding_users = cur.fetchone()[0]

    action = CreateUserAction(name="Alice")
    action.run(db)

    with db.conn as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM test_users_table;")
            count_after_adding_users = cur.fetchone()[0]

    assert count_after_adding_users == count_before_adding_users + 1

if __name__ == "__main__":
    from concurrent.futures import ProcessPoolExecutor
    os.environ["TEST_DATABASE__URL"] = "postgres://postgres@localhost:5432/postgres"
    
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
    
    db_ = TestDatabase()
    with db_.conn as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE test_users_table;")
    db_.teardown()

