from pydantic import BaseModel, HttpUrl, field_validator, ConfigDict
from typing import Optional

# Request body schema
class URLCreate(BaseModel):
    long_url: str
    custom_alias: str | None = None

    @field_validator("long_url", mode="before")
    @classmethod
    def ensure_protocol(cls, v):
        v = str(v)
        if not v.startswith("http://") and not v.startswith("https://"):
            v = "https://" + v
        return v

class URLResponse(BaseModel):
    short_url: str
    long_url: str

    model_config = ConfigDict(from_attributes=True)

# Response schema
class URLInfo(BaseModel):
    short_url: str
    long_url: str
