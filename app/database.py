import app.config as config
from supabase import create_client
from fastapi import Request
import redis.asyncio as redis

# Supabase anon client for user operations
anon_db = create_client(
    config.vars["supabase_url"],
    config.vars["supabase_anon_key"]
)

# Supabase system client for admin operations
adm_db = create_client(
    config.vars["supabase_url"],
    config.vars["supabase_secret_key"]
)

cache = redis.from_url(config.vars['redis_url'], encoding="utf-8", decode_responses=True)

def get_cache():
    """Returns Redis client for caching"""
    return cache

def get_adm_db():
    """Returns Supabase admin client for admin operations"""
    return adm_db

def get_anon_db():
    """Returns Supabase client for user level operations"""
    return anon_db

def get_auth_db(request: Request):
    """Returns authenticated Supabase client when used with router-level auth"""
    client = get_anon_db()
    
    # Get auth header from request
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        client.postgrest.auth(token)
    
    return client