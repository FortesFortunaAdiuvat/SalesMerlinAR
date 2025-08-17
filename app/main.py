from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import os

from . import models, schemas
from .database import SessionLocal, engine
from .email_utils import fetch_imap_emails, fetch_mailhog_emails

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rollodex Auto-Responder")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contacts", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.get("/contacts", response_model=list[schemas.Contact])
def list_contacts(source_type: str | None = None, marketing_intent: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Contact)
    if source_type:
        query = query.filter(models.Contact.source_type == source_type)
    if marketing_intent:
        query = query.filter(models.Contact.marketing_intent == marketing_intent)
    return query.all()


@app.post("/auto-responder/{contact_id}")
def send_auto_response(contact_id: int, db: Session = Depends(get_db)):
    contact = db.get(models.Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    # Placeholder for sending email
    return {"message": f"Auto-response sent to {contact.email}"}


@app.get("/emails/gmail")
def get_gmail_emails(limit: int = 10):
    username = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASS")
    if not username or not password:
        raise HTTPException(status_code=500, detail="Gmail credentials not configured")
    return fetch_imap_emails("imap.gmail.com", username, password, limit=limit)


@app.get("/emails/protonmail")
def get_proton_emails(limit: int = 10):
    username = os.getenv("PROTON_USER")
    password = os.getenv("PROTON_PASS")
    host = os.getenv("PROTON_HOST", "127.0.0.1")
    if not username or not password:
        raise HTTPException(status_code=500, detail="ProtonMail credentials not configured")
    return fetch_imap_emails(host, username, password, limit=limit)


@app.get("/emails/local")
def get_local_emails(limit: int = 10):
    base_url = os.getenv("MAILHOG_BASE_URL", "http://mailhog:8025")
    try:
        return fetch_mailhog_emails(base_url, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Local mail server error: {e}")
