from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.mobility import Mobility
from app.schemas.mobility import MobilityCreate, MobilityResponse

router = APIRouter(
    prefix="/mobility",
    tags=["Mobility"],
)


def build_location(latitude: float, longitude: float):
    return from_shape(
        Point(longitude, latitude),
        srid=4326,
    )


@router.get(
    "",
    response_model=list[MobilityResponse],
)
def list_mobility(
    type: str | None = Query(default=None),
    status_value: str | None = Query(default=None, alias="status"),
    locality: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = select(Mobility).order_by(Mobility.name)

    if type:
        query = query.where(Mobility.type.ilike(type))

    if status_value:
        query = query.where(Mobility.status.ilike(status_value))

    if locality:
        query = query.where(Mobility.locality.ilike(locality))

    return db.scalars(query).all()


@router.get(
    "/nearby",
    response_model=list[MobilityResponse],
)
def nearby_mobility(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    radius_km: float = Query(default=5, gt=0, le=100),
    db: Session = Depends(get_db),
):
    point = build_location(latitude, longitude)

    query = (
        select(Mobility)
        .where(
            Mobility.location.is_not(None),
            Mobility.location.distance_centroid(point)
            <= radius_km * 1000,
        )
        .order_by(
            Mobility.location.distance_centroid(point)
        )
    )

    return db.scalars(query).all()


@router.get(
    "/{mobility_id}",
    response_model=MobilityResponse,
)
def get_mobility(
    mobility_id: UUID,
    db: Session = Depends(get_db),
):
    mobility = db.get(Mobility, mobility_id)

    if not mobility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de movilidad no encontrado",
        )

    return mobility


@router.post(
    "",
    response_model=MobilityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_mobility(
    payload: MobilityCreate,
    db: Session = Depends(get_db),
):
    mobility = Mobility(
        type=payload.type,
        name=payload.name,
        description=payload.description,
        status=payload.status,
        address=payload.address,
        locality=payload.locality,
        latitude=payload.latitude,
        longitude=payload.longitude,
        is_simulated=payload.is_simulated,
    )

    if payload.latitude is not None and payload.longitude is not None:
        mobility.location = build_location(
            payload.latitude,
            payload.longitude,
        )

    db.add(mobility)
    db.commit()
    db.refresh(mobility)

    return mobility
