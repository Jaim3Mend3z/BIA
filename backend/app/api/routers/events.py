from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventResponse

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


def build_location(latitude: float, longitude: float):
    return from_shape(
        Point(longitude, latitude),
        srid=4326,
    )


@router.get(
    "",
    response_model=list[EventResponse],
)
def list_events(
    category: str | None = Query(default=None),
    locality: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = select(Event).order_by(Event.start_datetime)

    if category:
        query = query.where(Event.category.ilike(category))

    if locality:
        query = query.where(Event.locality.ilike(locality))

    return db.scalars(query).all()


@router.get(
    "/nearby",
    response_model=list[EventResponse],
)
def nearby_events(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    radius_km: float = Query(default=5, gt=0, le=100),
    db: Session = Depends(get_db),
):
    point = build_location(latitude, longitude)

    query = (
        select(Event)
        .where(
            Event.location.is_not(None),
            Event.location.distance_centroid(point)
            <= radius_km * 1000,
        )
        .order_by(
            Event.location.distance_centroid(point)
        )
    )

    return db.scalars(query).all()


@router.get(
    "/{event_id}",
    response_model=EventResponse,
)
def get_event(
    event_id: UUID,
    db: Session = Depends(get_db),
):
    event = db.get(Event, event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado",
        )

    return event


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
):
    event = Event(
        name=payload.name,
        description=payload.description,
        category=payload.category,
        start_datetime=payload.start_datetime,
        end_datetime=payload.end_datetime,
        address=payload.address,
        locality=payload.locality,
        latitude=payload.latitude,
        longitude=payload.longitude,
        source=payload.source,
        is_simulated=payload.is_simulated,
    )

    if payload.latitude is not None and payload.longitude is not None:
        event.location = build_location(
            payload.latitude,
            payload.longitude,
        )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event
