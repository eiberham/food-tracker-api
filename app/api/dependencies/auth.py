from fastapi import Depends, HTTPException, status
from typing import Annotated
from app.database import get_db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_supabase_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    """Verify Supabase JWT token and return authenticated client"""
    try:
        token = credentials.credentials
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")

        try:
            # Create authenticated client
            db = get_db()
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