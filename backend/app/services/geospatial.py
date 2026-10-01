from sqlalchemy import func, select
from geoalchemy2.shape import from_shape
from shapely.geometry import Point


def build_location(latitude: float, longitude: float):
    return from_shape(
        Point(longitude, latitude),
        srid=4326,
    )


def nearby_query(
    model,
    latitude: float,
    longitude: float,
    radius_km: float,
):
    point = build_location(latitude, longitude)
    radius_meters = radius_km * 1000

    distance = func.ST_Distance(
        model.location,
        point,
    )

    return (
        select(model)
        .where(
            model.location.is_not(None),
            func.ST_DWithin(
                model.location,
                point,
                radius_meters,
            ),
        )
        .order_by(distance)
    )
