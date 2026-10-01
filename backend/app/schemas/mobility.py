from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MobilityBase(BaseModel):
    type: str = Field(min_length=2, max_length=80)
    name: str = Field(min_length=2, max_length=200)
    description: str | None = None
    status: str = Field(min_length=2, max_length=80)
    address: str | None = Field(default=None, max_length=300)
    locality: str | None = Field(default=None, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    is_simulated: bool = True


class MobilityCreate(MobilityBase):
    pass


class MobilityResponse(MobilityBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    updated_at: datetime
