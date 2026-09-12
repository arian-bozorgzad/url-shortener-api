from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class LinkCreate(BaseModel):
    url: HttpUrl
    custom_code: str | None = Field(default=None, min_length=3, max_length=20, pattern=r"^[A-Za-z0-9_-]+$")


class LinkRead(BaseModel):
    id: int
    original_url: str
    short_code: str
    click_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LinkStats(LinkRead):
    last_accessed: datetime | None
