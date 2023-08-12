"""This reduces the flakiness of the test by improving the implementation to
introdcue a retry mechanism. However this is not a fully reliable solution but
will drastically reduce the likelihood of the test failing due to a network call.
"""
import requests
from backoff import on_exception, expo, full_jitter


class UnsuccessfulResponseError(Exception):
    """Raised when a response has an unsuccessful status code."""


def unsuppressed_get(url):
    res = requests.get(url)
    if res.status_code != 200:
        raise UnsuccessfulResponseError(f"Unexpected status code {res.status_code}")
    return res


def robust_query_web_server():
    retry_handler = on_exception(
        wait_gen=expo,
        exception=UnsuccessfulResponseError,
        max_tries=6,
        max_time=30,
        jitter=full_jitter,
    )
    response = retry_handler(unsuppressed_get)("https://example.com")
    return response.status_code


def test_query_web_server():
    status_code = robust_query_web_server()
    assert status_code == 200, f"Expected status code 200, but got {status_code}"
