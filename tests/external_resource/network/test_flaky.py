import requests

def query_web_server():
    response = requests.get("https://example.com")
    return response.status_code

def test_query_web_server():
    status_code = query_web_server()
    assert status_code == 200, f"Expected status code 200, but got {status_code}"
