import os

os.environ["DATABASE_URL"] = "sqlite:///./test_shortener.db"

from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module():
    if os.path.exists("test_shortener.db"):
        os.remove("test_shortener.db")


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "URL Shortener API is running"


def test_create_redirect_and_stats():
    response = client.post(
        "/links",
        json={"url": "https://example.com/docs", "custom_code": "notes1"},
    )
    assert response.status_code == 201
    assert response.json()["short_code"] == "notes1"

    redirect = client.get("/notes1", follow_redirects=False)
    assert redirect.status_code == 307
    assert redirect.headers["location"] == "https://example.com/docs"

    stats = client.get("/links/notes1/stats")
    assert stats.status_code == 200
    assert stats.json()["click_count"] == 1
    assert stats.json()["last_accessed"] is not None


def test_duplicate_custom_code():
    first = client.post("/links", json={"url": "https://example.com", "custom_code": "abc123"})
    second = client.post("/links", json={"url": "https://python.org", "custom_code": "abc123"})

    assert first.status_code == 201
    assert second.status_code == 409
