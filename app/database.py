import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  # no-op on Render; helpful locally

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:pass@db:5432/url_shortener"  # local Docker fallback
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # checks stale connections automatically
    pool_recycle=300      # refreshes every 5 min (helps with Neon auto-pause)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
