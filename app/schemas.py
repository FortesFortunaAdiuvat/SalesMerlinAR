from typing import Optional, Dict
from pydantic import BaseModel, EmailStr


class ContactBase(BaseModel):
    name: str
    email: EmailStr
    source_type: Optional[str] = None
    marketing_intent: Optional[str] = None
    social_media: Optional[Dict[str, str]] = None


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True
