from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ReportCreate(BaseModel):
    category: str = Field(min_length=2, max_length=100)
    title: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=5)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    address: str | None = Field(default=None, max_length=300)


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    category: str
    title: str
    description: str
    status: str
    latitude: float
    longitude: float
    address: str | None
    created_at: datetime
    updated_at: datetime


class ReportImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    report_id: UUID
    file_path: str
    created_at: datetime
