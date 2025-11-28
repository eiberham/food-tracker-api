import os
from dotenv import load_dotenv

load_dotenv()

vars = {
    "db_url": os.getenv("DB_URL")
}