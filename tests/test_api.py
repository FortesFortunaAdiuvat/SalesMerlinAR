import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app, get_db
from app.database import Base
from app import models

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_create_and_list_contacts(client):
    contact = {
        "name": "Alice",
        "email": "alice@example.com",
        "source_type": "website",
        "marketing_intent": "promo",
        "social_media": {"twitter": "https://twitter.com/alice"},
    }
    response = client.post("/contacts", json=contact)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == contact["email"]

    list_response = client.get("/contacts")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_filter_contacts(client):
    contacts = [
        {
            "name": "Alice",
            "email": "alice@example.com",
            "source_type": "website",
            "marketing_intent": "promo",
        },
        {
            "name": "Bob",
            "email": "bob@example.com",
            "source_type": "referral",
            "marketing_intent": "news",
        },
    ]
    for c in contacts:
        client.post("/contacts", json=c)

    resp = client.get("/contacts", params={"source_type": "website"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    resp = client.get("/contacts", params={"marketing_intent": "news"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_auto_responder(client):
    contact = {
        "name": "Alice",
        "email": "alice@example.com",
    }
    create_resp = client.post("/contacts", json=contact)
    contact_id = create_resp.json()["id"]

    resp = client.post(f"/auto-responder/{contact_id}")
    assert resp.status_code == 200
    assert "Auto-response sent" in resp.json()["message"]


def test_gmail_endpoint(client, monkeypatch):
    sample = [{"subject": "Hello"}]
    monkeypatch.setenv("GMAIL_USER", "user")
    monkeypatch.setenv("GMAIL_PASS", "pass")
    monkeypatch.setattr("app.main.fetch_imap_emails", lambda host, username, password, folder="INBOX", limit=10: sample)
    resp = client.get("/emails/gmail")
    assert resp.status_code == 200
    assert resp.json() == sample


def test_proton_endpoint(client, monkeypatch):
    sample = [{"subject": "Hi"}]
    monkeypatch.setenv("PROTON_USER", "user")
    monkeypatch.setenv("PROTON_PASS", "pass")
    monkeypatch.setattr("app.main.fetch_imap_emails", lambda host, username, password, folder="INBOX", limit=10: sample)
    resp = client.get("/emails/protonmail")
    assert resp.status_code == 200
    assert resp.json() == sample


def test_local_email_endpoint(client, monkeypatch):
    sample = [{"subject": "Local"}]
    monkeypatch.setattr("app.main.fetch_mailhog_emails", lambda base_url, limit=10: sample)
    resp = client.get("/emails/local")
    assert resp.status_code == 200
    assert resp.json() == sample
