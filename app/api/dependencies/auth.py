from fastapi import Depends, HTTPException, status, Header
from typing import Annotated
from app.database import get_anon_db, get_adm_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import app.config as config

security = HTTPBearer()

async def verify_supabase_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    """Verify Supabase JWT token and return authenticated client"""
    try:
        token = credentials.credentials
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")

        try:
            # Create authenticated client
            db = get_anon_db()
            db.postgrest.auth(token)
            
            # Verify the token
            user_response = db.auth.get_user(token)
            
            if not user_response.user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            
            # Return the authenticated client (this is what gets injected)
            return db
            
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token verification failed: {str(e)}")
    
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    

async def verify_cron_secret(x_cron_secret: str = Header(...)):
    """Verify the cron secret key from headers"""
    cron_secret_key = config.vars["cron_secret_key"]
    if x_cron_secret != cron_secret_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid cron secret key")
    
    db = get_adm_db()
    return db