import app.config as config
from supabase import create_client
from fastapi import Request

# Supabase client for all database operations
db = create_client(
    config.vars["supabase_url"],
    config.vars["supabase_anon_key"]
)

def get_db():
    """Returns Supabase client for all operations"""
    return db

def get_authenticated_db(request: Request):
    """Returns authenticated Supabase client when used with router-level auth"""
    client = db
    
    # Get auth header from request
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        client.postgrest.auth(token)
    
    return client