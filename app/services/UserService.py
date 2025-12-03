import bcrypt
from app.schemas.User import UserCreate, UserUpdate, UserResponse
from app.models.User import User
from sqlalchemy.orm import Session

class UserService:

    @classmethod
    def hash(cls, string: str) :
        bytes = string.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt).decode('utf-8')
        return hash

    @classmethod
    def create_user(cls, db: Session, payload: UserCreate) :
        try:
            exists = cls.get_user_by_username(db, payload.username) or cls.get_user_by_email(db, payload.email)
            if exists:
                raise Exception("Username or email already exists")
            
            hash = cls.hash(payload.password)
            data = payload.model_dump(exclude={'password'})
            data['password'] = hash
            user = User(**data)

            db.add(user)
            db.commit()
            db.refresh(user)
            
            return user 
        except Exception as e:
            db.rollback()  # rollback on error
            raise e
        
    @classmethod
    def update_user(cls, db: Session, user_id: int, payload: UserUpdate):
        try:
            user = cls.get_user_by_id(db, user_id)
            if not user:
                return None
            
            for key, value in payload.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            
            db.commit()
            db.refresh(user)
            return user
        
        except Exception as e:
            db.rollback()
            raise e
    
    @classmethod
    def list_users(cls, db: Session) :
        users = db.query(User).all()
        return users
    
    @classmethod
    def get_user_by_id(cls, db: Session, user_id: int) :
        user = db.query(User).filter(User.id == user_id).first()
        return user
    
    @classmethod
    def get_user_by_username(cls, db: Session, username: str):
        user = db.query(User).filter(User.username == username).first()
        return user
    
    @classmethod
    def get_user_by_email(cls, db: Session, email: str):
        user = db.query(User).filter(User.email == email).first()
        return user
    
    @classmethod
    def delete_user(cls, db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False