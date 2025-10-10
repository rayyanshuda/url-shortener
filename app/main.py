import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, schemas
from .utils import generate_short_code
from starlette.datastructures import URL

load_dotenv()  # read .env file

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Shortener API. Go to /docs to try it out."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}


from app.database import Base, engine, DATABASE_URL
from .models import URL

print("Connected Database URL:", DATABASE_URL)

# Create the table(s) if they don’t already exist
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")




@app.post("/shorten")
def create_short_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    # 1️⃣ Check if custom alias provided
    if url.custom_alias:
        # Check if alias already exists
        existing = db.query(models.URL).filter(models.URL.short_code == url.custom_alias).first()
        if existing:
            raise HTTPException(status_code=400, detail="Custom alias already exists. Please choose another one.")
        short_code = url.custom_alias
    else:
        # Otherwise generate a random one
        short_code = generate_short_code()

    # 2️⃣ Create and save to database
    db_url = models.URL(short_code=short_code, long_url=url.long_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    # 3️⃣ Build full short URL
    short_url = f"{BASE_URL}/{short_code}"
    return {"short_url": short_url, "long_url": url.long_url}




@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    # Look up short code
    url_entry = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # Increment click count
    url_entry.clicks += 1
    db.commit()

    # Ensure URL starts with scheme
    long_url = url_entry.long_url
    if not long_url.startswith(("http://", "https://")):
        long_url = "https://" + long_url

    # Redirect safely
    return RedirectResponse(url=long_url)

