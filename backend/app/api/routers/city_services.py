from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.city_service import CityService
from app.schemas.city_service import (
    CityServiceCreate,
    CityServiceResponse,
)
from app.services.geospatial import build_location, nearby_query

router = APIRouter(
    prefix="/city-services",
    tags=["City Services"],
)


@router.get(
    "",
    response_model=list[CityServiceResponse],
)
def list_city_services(
    category: str | None = Query(default=None),
    locality: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = select(CityService).order_by(CityService.name)

    if category:
        query = query.where(CityService.category.ilike(category))

    if locality:
        query = query.where(CityService.locality.ilike(locality))

    return db.scalars(query).all()


@router.get(
    "/nearby",
    response_model=list[CityServiceResponse],
)
def nearby_city_services(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    radius_km: float = Query(default=5, gt=0, le=100),
    db: Session = Depends(get_db),
):
    query = nearby_query(
        CityService,
        latitude,
        longitude,
        radius_km,
    )

    return db.scalars(query).all()


@router.get(
    "/{service_id}",
    response_model=CityServiceResponse,
)
def get_city_service(
    service_id: UUID,
    db: Session = Depends(get_db),
):
    service = db.get(CityService, service_id)

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio ciudadano no encontrado",
        )

    return service


@router.post(
    "",
    response_model=CityServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_city_service(
    payload: CityServiceCreate,
    db: Session = Depends(get_db),
):
    service = CityService(
        name=payload.name,
        category=payload.category,
        description=payload.description,
        address=payload.address,
        locality=payload.locality,
        latitude=payload.latitude,
        longitude=payload.longitude,
        phone=payload.phone,
        website=payload.website,
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
