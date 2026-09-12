# URL Shortener REST API

A small backend project built with **FastAPI**, **SQLAlchemy**, and **SQLite**. It creates short URLs, redirects them to the original address, and keeps basic click statistics.

I built this project to practice REST APIs, database storage, redirects, validation, and handling duplicate short codes.

## Features

- Create a short URL from a normal URL
- Optional custom short code
- Redirect short links to the original URL
- Count how many times each link is opened
- Store the last access time
- View basic statistics for a link
- Detect duplicate short codes
- Delete links
- Basic 404 and conflict responses
- Swagger API documentation

## Project structure

```text
url-shortener-api/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_api.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Run locally

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the API

```bash
uvicorn app.main:app --reload
```

Open Swagger docs at:

```text
http://127.0.0.1:8000/docs
```

The SQLite database is created automatically when the app starts.

## Example

Create a short link:

```json
POST /links
{
  "url": "https://example.com/some/long/page"
}
```

Or choose a custom code:

```json
POST /links
{
  "url": "https://example.com/notes",
  "custom_code": "notes1"
}
```

Then open:

```text
http://127.0.0.1:8000/notes1
```

Check statistics:

```text
GET /links/notes1/stats
```

## Tests

```bash
pytest
```

The tests cover creating links, redirects, click tracking, statistics, and duplicate-code handling.
