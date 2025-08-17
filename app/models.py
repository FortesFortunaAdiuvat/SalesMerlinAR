from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.sqlite import JSON

from .database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    source_type = Column(String, index=True)
    marketing_intent = Column(String, index=True)
    social_media = Column(JSON, nullable=True)
