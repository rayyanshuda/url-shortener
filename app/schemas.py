from pydantic import BaseModel, HttpUrl

# Request body schema
class URLCreate(BaseModel):
    long_url: str   # ensures valid URL

# Response schema
class URLInfo(BaseModel):
    short_url: str
    long_url: str
