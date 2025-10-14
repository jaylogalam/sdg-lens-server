import requests
from conftest import host_url

def test_signup():
    data = {
        "email": "example@gmail.com",
        "password": "123456"
    }

    print(requests.post(f"{host_url}/signup/password", json=data).json())

if __name__ == "__main__":
    test_signup()