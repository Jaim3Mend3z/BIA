from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str | None = None
    category: str = Field(min_length=2, max_length=80)
    start_datetime: datetime
    end_datetime: datetime | None = None
    address: str | None = Field(default=None, max_length=300)
    locality: str | None = Field(default=None, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    source: str | None = Field(default=None, max_length=200)
    is_simulated: bool = True


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
