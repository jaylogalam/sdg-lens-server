from typing import Annotated
from fastapi.params import Depends
from database import get_db, Client
from models import AuthModel

class AuthServices:
    class Signup:
        @staticmethod
        def with_password(creds: AuthModel.Signup, db: Annotated[Client, Depends(get_db)]):
            db.auth.sign_up({
                "email": creds.email,
                "password": creds.password
            })

    class Login:
        ...

    class Utils:
        ...        
        # @classmethod
        # def check_email_exists(cls, email: str) -> bool:
        #     user = cls.auth.
        #     return user