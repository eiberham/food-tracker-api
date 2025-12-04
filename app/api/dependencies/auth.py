from fastapi import Depends, HTTPException, status
from typing import Annotated
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
import app.config as config
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.user_service import UserService

security = HTTPBearer()

async def verify_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], db: Annotated[Session, Depends(get_db)]):
    try:
        token = credentials.credentials
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
        payload = jwt.decode(token, config.vars['jwt_secret_key'], algorithms=[config.vars['jwt_algorithm']])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user = UserService.get_user_by_id(db, int(user_id))
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        return user
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token verification failed")