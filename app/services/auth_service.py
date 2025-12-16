from app.database import db
from app.schemas.auth import AuthenticationResponse, AuthenticationUser

class AuthService:
     
    @classmethod
    def login(cls, email: str, password: str):
        response = db.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if response.session is None:
            raise Exception("No session returned")

        response = AuthenticationResponse(
            access_token = response.session.access_token,
            refresh_token= response.session.refresh_token,
            expires_in= response.session.expires_in,
            user= AuthenticationUser(id=response.user.id, email=response.user.email)
        )

        return response