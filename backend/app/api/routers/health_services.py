from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.health_service import HealthService
from app.schemas.health_service import (
    HealthServiceCreate,
    HealthServiceResponse,
)

router = APIRouter(
    prefix="/health-services",
    tags=["Health Services"],
)


def build_location(latitude: float, longitude: float):
    return from_shape(
        Point(longitude, latitude),
        srid=4326,
    )


@router.get(
    "",
    response_model=list[HealthServiceResponse],
)
def list_health_services(
    type: str | None = Query(default=None),
    locality: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = select(HealthService).order_by(HealthService.name)

    if type:
        query = query.where(HealthService.type.ilike(type))

    if locality:
        query = query.where(HealthService.locality.ilike(locality))

    return db.scalars(query).all()


@router.get(
    "/nearby",
    response_model=list[HealthServiceResponse],
)
def nearby_health_services(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    radius_km: float = Query(default=5, gt=0, le=100),
    db: Session = Depends(get_db),
):
    point = build_location(latitude, longitude)

    query = (
        select(HealthService)
        .where(
            HealthService.location.is_not(None),
            HealthService.location.distance_centroid(point)
            <= radius_km * 1000,
        )
        .order_by(
            HealthService.location.distance_centroid(point)
        )
    )

    return db.scalars(query).all()


@router.get(
    "/{service_id}",
    response_model=HealthServiceResponse,
)
def get_health_service(
    service_id: UUID,
    db: Session = Depends(get_db),
):
    service = db.get(HealthService, service_id)

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio de salud no encontrado",
        )

    return service


@router.post(
    "",
    response_model=HealthServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_health_service(
    payload: HealthServiceCreate,
    db: Session = Depends(get_db),
):
    service = HealthService(
        name=payload.name,
        type=payload.type,
        description=payload.description,
        address=payload.address,
        locality=payload.locality,
        latitude=payload.latitude,
        longitude=payload.longitude,
        phone=payload.phone,
        opening_hours=payload.opening_hours,
        services=payload.services,
        is_simulated=payload.is_simulated,
    )

    if payload.latitude is not None and payload.longitude is not None:
        service.location = build_location(
            payload.latitude,
            payload.longitude,
        )

    db.add(service)
    db.commit()
    db.refresh(service)

    return service
