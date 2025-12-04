from jose import jwt
from datetime import datetime, timedelta, timezone
import bcrypt
import app.config as config
from sqlalchemy.orm import Session

from app.models.user import User

class AuthService:

    @classmethod
    def create_jwt(cls, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=config.vars['access_token_expire_minutes'])
        }
        token = jwt.encode(payload, config.vars['jwt_secret_key'], algorithm=config.vars['jwt_algorithm'])
        return token
    
    @classmethod
    def check_password(cls, password, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @classmethod
    def login(cls, db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None

        if cls.check_password(password, user.password):
            token = cls.create_jwt(user.id)
            return token
        return None