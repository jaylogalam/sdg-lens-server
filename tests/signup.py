import requests
from conftest import host_url

def test_signup():
    data1 = dict(
        username= "user",
        email= "example@gmail.com",
        password= "123456"
    )

    response = requests.post(f"{host_url}signup/password", data=data1)
    print(response.text, response.status_code)

if __name__ == "__main__":
    test_signup()