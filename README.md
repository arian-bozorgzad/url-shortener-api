# URL Shortener REST API

A small URL shortener backend built with FastAPI and SQLite.

The API creates short links, redirects users to the original URL and keeps basic click statistics.

## Features

- Create short URLs
- Use an optional custom short code
- Redirect to the original URL
- Count link clicks
- Show basic link statistics
- Check for duplicate short codes
- Basic error handling

## Built with

- Python
- FastAPI
- SQLite
- SQLAlchemy

## Run the project

Install the requirements:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Tests

```bash
pytest
```
