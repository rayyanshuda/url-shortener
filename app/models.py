from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(100), unique=True, index=True, nullable=False)
    long_url = Column(String, nullable=False)
    custom_alias = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    clicks = Column(Integer, default=0)
    
