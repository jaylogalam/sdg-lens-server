from database import db

class AuthServices:
    class Signup:
        @staticmethod
        def with_password(email: str, password: str):
            db.auth.sign_up({"email": email, "password": password})

    class Login:
        ...