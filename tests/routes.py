import requests
from conftest import host_url

def test_server():
    print(requests.get(f"{host_url}").json())

def test_convert():
    print(requests.get(f"{host_url}/convert/text").json())

if __name__ == "__main__":
    test_convert()
