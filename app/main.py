import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import SessionLocal
from . import models, schemas
from .utils import generate_short_code
#from starlette.datastructures import URL

load_dotenv()  # read .env file

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the URL Shortener API. Go to /docs to try it out."}

@app.get("/health")
async def health_check():
    return {"status": "ok"}


from .database import Base, engine, DATABASE_URL

# Create the table(s) if they don’t already exist
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


MAX_TRIES = 5  # max attempts to avoid short code collision

@app.post("/shorten")
def create_short_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    if url.custom_alias and len(url.custom_alias) > 100:
        raise HTTPException(status_code=400, detail="Alias too long (max 100 characters).")

    # --- Custom alias path: try once, fail if taken ---
    if url.custom_alias:
        try:
            db_url = models.URL(short_code=url.custom_alias, long_url=url.long_url)
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Custom alias already exists. Please choose another one.")

    # --- Auto-generate path: retry on rare collisions ---
    else:
        for _ in range(MAX_TRIES):
            code = generate_short_code()
            try:
                db_url = models.URL(short_code=code, long_url=url.long_url)
                db.add(db_url)
                db.commit()
                db.refresh(db_url)
                break
            except IntegrityError:
                db.rollback()  # duplicate short_code—try again
        else:
            raise HTTPException(status_code=500, detail="Failed to generate a unique short code. Please try again.")

    short_url = f"{BASE_URL}/{db_url.short_code}"
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

