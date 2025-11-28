from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import app.config as config

DATABASE_URL = config.vars["db_url"]

#sqlalchemy setup
engine = create_engine(DATABASE_URL)

#session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base class for orm models
Base = declarative_base()

#dependency to get db session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

