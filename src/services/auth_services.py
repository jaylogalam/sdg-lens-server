from supabase import Client
from models import AuthModel

class AuthServices:
    class Signup:
        @staticmethod
        def with_password(creds: AuthModel.Signup, db: Client):
            response = db.auth.sign_up({
                "email": creds.email,
                "password": creds.password
            })

            user = response.user
            if not user:
                raise Exception("Signup failed: No user returned")

            init_profile = AuthModel.InitProfile(
                id=user.id,
                created_at=user.created_at,
                username=creds.username
            )

            response = db.table("profiles").insert(init_profile.model_dump(mode="json")).execute()

    class Login:
        ...

    class Utils:
        ...        
        # @classmethod
        # def check_email_exists(cls, email: str) -> bool:
        #     user = cls.auth.
        #     return user