from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.place import Place
from app.schemas.place import PlaceCreate, PlaceResponse

router = APIRouter(
    prefix="/places",
    tags=["Places"],
)


def build_location(latitude: float, longitude: float):
    return from_shape(
        Point(longitude, latitude),
        srid=4326,
    )


@router.get(
    "",
    response_model=list[PlaceResponse],
)
def list_places(
    category: str | None = Query(default=None),
    locality: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = select(Place).order_by(Place.name)

    if category:
        query = query.where(Place.category.ilike(category))

    if locality:
        query = query.where(Place.locality.ilike(locality))

    return db.scalars(query).all()


@router.get(
    "/nearby",
    response_model=list[PlaceResponse],
)
def nearby_places(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    radius_km: float = Query(default=5, gt=0, le=100),
    db: Session = Depends(get_db),
):
    point = build_location(latitude, longitude)

    query = (
        select(Place)
        .where(
            Place.location.is_not(None),
            Place.location.distance_centroid(point)
            <= radius_km * 1000,
        )
        .order_by(
            Place.location.distance_centroid(point)
        )
    )

    return db.scalars(query).all()


@router.get(
    "/{place_id}",
    response_model=PlaceResponse,
)
def get_place(
    place_id: UUID,
    db: Session = Depends(get_db),
):
    place = db.get(Place, place_id)

    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lugar no encontrado",
        )

    return place


@router.post(
    "",
    response_model=PlaceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_place(
    payload: PlaceCreate,
    db: Session = Depends(get_db),
):
    place = Place(
        name=payload.name,
        category=payload.category,
        description=payload.description,
        address=payload.address,
        locality=payload.locality,
        latitude=payload.latitude,
        longitude=payload.longitude,
        phone=payload.phone,
        opening_hours=payload.opening_hours,
        is_simulated=payload.is_simulated,
    )

    if payload.latitude is not None and payload.longitude is not None:
        place.location = build_location(
            payload.latitude,
            payload.longitude,
        )

    db.add(place)
    db.commit()
    db.refresh(place)

    return place
