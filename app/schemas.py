from typing import Optional, Dict, List
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


class CampaignTouchpointBase(BaseModel):
    subject: str
    body: str
    delay_seconds: float


class CampaignTouchpointCreate(CampaignTouchpointBase):
    pass


class CampaignTouchpoint(CampaignTouchpointBase):
    id: int

    class Config:
        orm_mode = True


class CampaignBase(BaseModel):
    name: str


class CampaignCreate(CampaignBase):
    touchpoints: List[CampaignTouchpointCreate]


class Campaign(CampaignBase):
    id: int
    touchpoints: List[CampaignTouchpoint] = []

    class Config:
        orm_mode = True
