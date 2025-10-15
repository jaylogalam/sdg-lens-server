from database import SupabaseClient

_auth = SupabaseClient.get_client().auth

class AuthServices:
    class Signup:
        @classmethod
        def with_password(cls, email: str, password: str):
            _auth.sign_up({"email": email, "password": password})

    class Login:
        ...

    class Utils:
        ...        
        # @classmethod
        # def check_email_exists(cls, email: str) -> bool:
        #     user = cls.auth.
        #     return user