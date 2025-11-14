from fastapi import Request

class Auth:
    @staticmethod
    def get_token(request: Request):
        try:
            token = request.cookies.get("access_token")

            if token and token.startswith('Bearer '):
                token = token[7:]

            if not token:
                return ""

            return token
        
        except Exception as e:
            raise Exception(f"Error getting user: {e}")

    @staticmethod
    def get_role(request: Request):
        ...