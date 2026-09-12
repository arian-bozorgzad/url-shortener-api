import random
import string
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A simple API for creating short links and tracking clicks.",
    version="1.0.0",
)


def make_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def find_link(db: Session, code: str):
    return db.scalar(select(models.Link).where(models.Link.short_code == code))


@app.get("/")
def root():
    return {"message": "URL Shortener API is running"}


@app.post("/links", response_model=schemas.LinkRead, status_code=status.HTTP_201_CREATED)
def create_link(data: schemas.LinkCreate, db: Session = Depends(get_db)):
    # A custom code is useful for testing, otherwise just generate one.
    if data.custom_code:
        if find_link(db, data.custom_code):
            raise HTTPException(status_code=409, detail="Short code already exists")
        code = data.custom_code
    else:
        code = make_code()
        tries = 0
        while find_link(db, code) and tries < 8:
            code = make_code()
            tries += 1

        if tries == 8 and find_link(db, code):
            raise HTTPException(status_code=500, detail="Could not generate a unique short code")

    link = models.Link(original_url=str(data.url), short_code=code)
    db.add(link)

    try:
        db.commit()
    except IntegrityError:
        # Extra check in case two requests somehow get the same code.
        db.rollback()
        raise HTTPException(status_code=409, detail="Short code already exists")

    db.refresh(link)
    return link


@app.get("/links", response_model=list[schemas.LinkRead])
def list_links(db: Session = Depends(get_db)):
    return db.scalars(select(models.Link).order_by(models.Link.id.desc())).all()


@app.get("/links/{short_code}", response_model=schemas.LinkRead)
def get_link(short_code: str, db: Session = Depends(get_db)):
    link = find_link(db, short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")
    return link


@app.get("/links/{short_code}/stats", response_model=schemas.LinkStats)
def link_stats(short_code: str, db: Session = Depends(get_db)):
    link = find_link(db, short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")
    return link


@app.delete("/links/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(short_code: str, db: Session = Depends(get_db)):
    link = find_link(db, short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    db.delete(link)
    db.commit()


@app.get("/{short_code}", include_in_schema=False)
def open_short_link(short_code: str, db: Session = Depends(get_db)):
    link = find_link(db, short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")

    link.click_count += 1
    link.last_accessed = datetime.now(timezone.utc)
    db.commit()

    return RedirectResponse(url=link.original_url, status_code=307)
