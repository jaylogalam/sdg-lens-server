from supabase import Client
from fastapi.responses import JSONResponse
from utils.auth import AuthUtils

class AuthServices:
    class Signup:
        @staticmethod
        def with_password(db: Client, username: str, email: str, password: str):
            if AuthUtils.check_username_exists(username):
                raise ValueError("Username already exists")
            
            if AuthUtils.check_email_exists(email):
                raise ValueError("Email already exists")
            
            # Sign up the user
            db.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username,
                        "app_role": "user"
                    }
                }
            })

            # Set session
            response = AuthServices.Login.with_password(
                db=db,
                email=email,
                password=password
            )
            
            return response

    class Login:
        @staticmethod
        def with_password(db: Client, email: str, password: str):
            if not AuthUtils.check_email_exists(email):
                raise ValueError("Email does not exist")
            
            auth_response = db.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if not auth_response.session or not auth_response.session.access_token:
                raise ValueError("Login Failed")

            # Response
            access_token = auth_response.session.access_token
            response = JSONResponse("Login successful")
            response.set_cookie(
                key="access_token",
                path="/",
                value=f"Bearer {access_token}",
                httponly=True,
                secure=True,
                samesite="none"
            )
            
            return response

    class Logout:
        @staticmethod
        def logout(db: Client):
            db.auth.sign_out()
            response = JSONResponse("Logout successful")
            response.delete_cookie(
                key='access_token',
                path="/",
                httponly=True,
                secure=True,
                samesite="none"
            )
            
            return response