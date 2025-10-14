import requests
from conftest import host_url

def test_signup():
    data = {
        "email": "example@gmail.com",
        "password": "123456"
    }

    print(requests.get(f"{host_url}/signup/password").json())

if __name__ == "__main__":
    test_signup()