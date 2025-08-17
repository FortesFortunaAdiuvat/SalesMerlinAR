# SalesMerlinAR Rollodex Auto-Responder

This project provides a FastAPI-based auto-responder for managing a master email list and segmented lists by source type and marketing intent. Each contact can store optional social media links.

## Features
- Store contacts with name, email, source type, marketing intent, and social media links.
- List all contacts or filter by `source_type` and `marketing_intent`.
- Endpoint stub for sending an auto-response to a contact.
- SQLite database for persistence.
- Docker support for running the API and accessing the database separately.

## Setup

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```
3. The API will be available at `http://localhost:8000`.

### Docker
To run using Docker Compose:
```bash
docker-compose up --build
```
This starts the FastAPI app and a SQLite container that shares the database file via a volume.

## Testing
Run the unit tests with:
```bash
pytest
```

## Endpoints Overview
- `POST /contacts` – add a contact to the master list.
- `GET /contacts` – list contacts, optionally filtered by `source_type` and/or `marketing_intent`.
- `POST /auto-responder/{contact_id}` – send an auto-response (placeholder) to a contact.

The database file is stored under `data/rollodex.db` and can be accessed independently of the API.
