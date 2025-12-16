from pydantic import BaseModel

class AuthenticationRequest(BaseModel):
    email: str
    password: str

class AuthenticationUser(BaseModel):
    id: str
    email: str

class AuthenticationResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    expires_in: int | None = None
    token_type: str = "bearer"
    user: AuthenticationUser | None = None