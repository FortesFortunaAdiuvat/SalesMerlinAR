from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship

from .database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    source_type = Column(String, index=True)
    marketing_intent = Column(String, index=True)
    social_media = Column(JSON, nullable=True)


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    touchpoints = relationship(
        "CampaignTouchpoint", back_populates="campaign", cascade="all, delete-orphan"
    )


class CampaignTouchpoint(Base):
    __tablename__ = "campaign_touchpoints"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)
    delay_seconds = Column(Float, nullable=False, default=0)
    campaign = relationship("Campaign", back_populates="touchpoints")
