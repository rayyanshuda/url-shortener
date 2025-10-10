from pydantic import BaseModel, HttpUrl, validator
from typing import Optional

# Request body schema
class URLCreate(BaseModel):
    long_url: str
    custom_alias: str | None = None

    @validator("long_url")
    def ensure_protocol(cls, v):
        if not v.startswith("http://") and not v.startswith("https://"):
            v = "https://" + v
        return v

class URLResponse(BaseModel):
    short_url: str
    long_url: str

    class Config:
        orm_mode = True

# Response schema
class URLInfo(BaseModel):
    short_url: str
    long_url: str
