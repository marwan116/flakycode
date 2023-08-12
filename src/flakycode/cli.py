"""Flaky code cli."""
from typer import Typer

app = Typer()

@app.command()
def flaky():
    """Flaky code"""
    # TODO - implement cli
    print("This should exhibit flaky tests")

if __name__ == "__main__":
    app()