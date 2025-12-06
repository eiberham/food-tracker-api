import os
from dotenv import load_dotenv

load_dotenv()

vars = {
    "db_url": os.getenv("DB_URL"),
    "jwt_secret_key": os.getenv("JWT_SECRET_KEY"),
    "jwt_algorithm": os.getenv("JWT_ALGORITHM"),
    "access_token_expire_minutes": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)),
    "groq_api_key": os.getenv("GROQ_API_KEY"),
    "supabase_url": os.getenv("SUPABASE_URL"),
    "supabase_key": os.getenv("SUPABASE_KEY"),
    "redis_url": os.getenv("REDIS_URL"),
}