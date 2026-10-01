from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PlaceBase(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    category: str = Field(min_length=2, max_length=100)
    description: str | None = None
    address: str | None = Field(default=None, max_length=300)
    locality: str | None = Field(default=None, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    phone: str | None = Field(default=None, max_length=50)
    opening_hours: str | None = Field(default=None, max_length=500)
    is_simulated: bool = True


class PlaceCreate(PlaceBase):
    pass


class PlaceResponse(PlaceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
