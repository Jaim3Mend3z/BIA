from datetime import datetime, timezone

from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.city_service import CityService
from app.models.event import Event
from app.models.health_service import HealthService
from app.models.mobility import Mobility
from app.models.place import Place


def build_location(latitude: float, longitude: float):
    return from_shape(
        Point(longitude, latitude),
        srid=4326,
    )


def add_event(db, data):
    existing = db.scalar(
        select(Event).where(Event.name == data["name"])
    )

    if existing:
        return False

    event = Event(
        **data,
        location=build_location(
            data["latitude"],
            data["longitude"],
        ),
    )

    db.add(event)
    return True


def add_health_service(db, data):
    existing = db.scalar(
        select(HealthService).where(
            HealthService.name == data["name"]
        )
    )

    if existing:
        return False

    service = HealthService(
        **data,
        location=build_location(
            data["latitude"],
            data["longitude"],
        ),
    )

    db.add(service)
    return True


def add_place(db, data):
    existing = db.scalar(
        select(Place).where(Place.name == data["name"])
    )

    if existing:
        return False

    place = Place(
        **data,
        location=build_location(
            data["latitude"],
            data["longitude"],
        ),
    )

    db.add(place)
    return True


def add_city_service(db, data):
    existing = db.scalar(
        select(CityService).where(
            CityService.name == data["name"]
        )
    )

    if existing:
        return False

    service = CityService(
        **data,
        location=build_location(
            data["latitude"],
            data["longitude"],
        ),
    )

    db.add(service)
    return True


def add_mobility(db, data):
    existing = db.scalar(
        select(Mobility).where(
            Mobility.name == data["name"]
        )
    )

    if existing:
        return False

    mobility = Mobility(
        **data,
        location=build_location(
            data["latitude"],
            data["longitude"],
        ),
    )

    db.add(mobility)
    return True


def main():
    db = SessionLocal()

    try:
        event_date = datetime(
            2026,
            10,
            15,
            18,
            0,
            tzinfo=timezone.utc,
        )

        events = [
            {
                "name": "Festival Cultural BIA",
                "description": "Evento cultural simulado para pruebas de BIA.",
                "category": "cultural",
                "start_datetime": event_date,
                "end_datetime": datetime(
                    2026,
                    10,
                    15,
                    21,
                    0,
                    tzinfo=timezone.utc,
                ),
                "address": "Centro Cultural de Bogotá",
                "locality": "La Candelaria",
                "latitude": 4.5961,
                "longitude": -74.0721,
                "source": "BIA Demo",
                "is_simulated": True,
            },
            {
                "name": "Feria Educativa BIA",
                "description": "Feria académica simulada con actividades educativas.",
                "category": "educativo",
                "start_datetime": datetime(
                    2026,
                    10,
                    18,
                    15,
                    0,
                    tzinfo=timezone.utc,
                ),
                "end_datetime": datetime(
                    2026,
                    10,
                    18,
                    20,
                    0,
                    tzinfo=timezone.utc,
                ),
                "address": "Zona Universitaria",
                "locality": "Chapinero",
                "latitude": 4.6486,
                "longitude": -74.0628,
                "source": "BIA Demo",
                "is_simulated": True,
            },
            {
                "name": "Jornada Recreativa Bosa",
                "description": "Actividad recreativa simulada para la comunidad.",
                "category": "recreativo",
                "start_datetime": datetime(
                    2026,
                    10,
                    20,
                    14,
                    0,
                    tzinfo=timezone.utc,
                ),
                "end_datetime": datetime(
                    2026,
                    10,
                    20,
                    18,
                    0,
                    tzinfo=timezone.utc,
                ),
                "address": "Sector Central de Bosa",
                "locality": "Bosa",
                "latitude": 4.6309,
                "longitude": -74.1944,
                "source": "BIA Demo",
                "is_simulated": True,
            },
            {
                "name": "Encuentro Deportivo Kennedy",
                "description": "Actividad deportiva simulada.",
                "category": "deportivo",
                "start_datetime": datetime(
                    2026,
                    10,
                    24,
                    13,
                    0,
                    tzinfo=timezone.utc,
                ),
                "end_datetime": datetime(
                    2026,
                    10,
                    24,
                    18,
                    0,
                    tzinfo=timezone.utc,
                ),
                "address": "Zona deportiva Kennedy",
                "locality": "Kennedy",
                "latitude": 4.6294,
                "longitude": -74.1616,
                "source": "BIA Demo",
                "is_simulated": True,
            },
            {
                "name": "Feria Comunitaria de Suba",
                "description": "Feria comunitaria simulada con servicios y actividades.",
                "category": "comunitario",
                "start_datetime": datetime(
                    2026,
                    10,
                    28,
                    16,
                    0,
                    tzinfo=timezone.utc,
                ),
                "end_datetime": datetime(
                    2026,
                    10,
                    28,
                    20,
                    0,
                    tzinfo=timezone.utc,
                ),
                "address": "Centro de Suba",
                "locality": "Suba",
                "latitude": 4.7449,
                "longitude": -74.0933,
                "source": "BIA Demo",
                "is_simulated": True,
            },
        ]

        health_services = [
            {
                "name": "Centro de Salud BIA Norte",
                "type": "Centro de salud",
                "description": "Servicio de salud simulado para pruebas de BIA.",
                "address": "Sector Norte",
                "locality": "Barrios Unidos",
                "latitude": 4.6769,
                "longitude": -74.0703,
                "phone": "6010000010",
                "opening_hours": "Lunes a viernes 07:00-17:00",
                "services": {
                    "medicina_general": True,
                    "vacunacion": True,
                    "odontologia": False,
                },
                "is_simulated": True,
            },
            {
                "name": "Centro Médico BIA Chapinero",
                "type": "Centro médico",
                "description": "Centro médico simulado con atención general.",
                "address": "Sector Chapinero",
                "locality": "Chapinero",
                "latitude": 4.6462,
                "longitude": -74.0621,
                "phone": "6010000011",
                "opening_hours": "Lunes a sábado 08:00-18:00",
                "services": {
                    "medicina_general": True,
                    "vacunacion": True,
                    "urgencias": False,
                },
                "is_simulated": True,
            },
            {
                "name": "Punto de Salud BIA Bosa",
                "type": "Punto de atención",
                "description": "Punto de atención en salud simulado.",
                "address": "Zona central de Bosa",
                "locality": "Bosa",
                "latitude": 4.6318,
                "longitude": -74.1915,
                "phone": "6010000012",
                "opening_hours": "Lunes a viernes 07:30-16:30",
                "services": {
                    "medicina_general": True,
                    "vacunacion": True,
                    "odontologia": True,
                },
                "is_simulated": True,
            },
            {
                "name": "Centro de Atención BIA Suba",
                "type": "Centro de atención",
                "description": "Servicio de salud simulado en la localidad de Suba.",
                "address": "Zona central de Suba",
                "locality": "Suba",
                "latitude": 4.7461,
                "longitude": -74.0922,
                "phone": "6010000013",
                "opening_hours": "Lunes a viernes 07:00-18:00",
                "services": {
                    "medicina_general": True,
                    "vacunacion": False,
                    "odontologia": True,
                },
                "is_simulated": True,
            },
            {
                "name": "Punto de Vacunación BIA Kennedy",
                "type": "Vacunación",
                "description": "Punto de vacunación simulado.",
                "address": "Zona central de Kennedy",
                "locality": "Kennedy",
                "latitude": 4.6259,
                "longitude": -74.1624,
                "phone": "6010000014",
                "opening_hours": "Lunes a sábado 08:00-16:00",
                "services": {
                    "vacunacion": True,
                    "medicina_general": False,
                },
                "is_simulated": True,
            },
        ]

        places = [
            {
                "name": "Parque BIA Central",
                "category": "parque",
                "description": "Espacio recreativo simulado.",
                "address": "Zona Centro",
                "locality": "Santa Fe",
                "latitude": 4.6097,
                "longitude": -74.0703,
                "phone": "6010000020",
                "opening_hours": "Todos los días 06:00-20:00",
                "is_simulated": True,
            },
            {
                "name": "Biblioteca BIA Chapinero",
                "category": "biblioteca",
                "description": "Biblioteca pública simulada para consulta.",
                "address": "Sector Chapinero",
                "locality": "Chapinero",
                "latitude": 4.6489,
                "longitude": -74.0640,
                "phone": "6010000021",
                "opening_hours": "Lunes a sábado 08:00-18:00",
                "is_simulated": True,
            },
            {
                "name": "Museo BIA Histórico",
                "category": "museo",
                "description": "Museo simulado para actividades culturales.",
                "address": "Centro Histórico",
                "locality": "La Candelaria",
                "latitude": 4.5976,
                "longitude": -74.0761,
                "phone": "6010000022",
                "opening_hours": "Martes a domingo 09:00-17:00",
                "is_simulated": True,
            },
            {
                "name": "Centro Cultural BIA Suba",
                "category": "cultura",
                "description": "Espacio cultural simulado.",
                "address": "Centro de Suba",
                "locality": "Suba",
                "latitude": 4.7438,
                "longitude": -74.0917,
                "phone": "6010000023",
                "opening_hours": "Lunes a viernes 09:00-19:00",
                "is_simulated": True,
            },
            {
                "name": "Parque Comunitario BIA Bosa",
                "category": "parque",
                "description": "Parque comunitario simulado.",
                "address": "Zona central de Bosa",
                "locality": "Bosa",
                "latitude": 4.6298,
                "longitude": -74.1935,
                "phone": "6010000024",
                "opening_hours": "Todos los días 05:30-21:00",
                "is_simulated": True,
            },
        ]

        city_services = [
            {
                "name": "CADE BIA Centro",
                "category": "atencion_ciudadana",
                "description": "Punto de atención ciudadana simulado.",
                "address": "Sector Centro",
                "locality": "La Candelaria",
                "latitude": 4.5981,
                "longitude": -74.0758,
                "phone": "6010000030",
                "website": "https://bia.local",
                "is_simulated": True,
            },
            {
                "name": "Punto BIA Chapinero",
                "category": "tramites",
                "description": "Punto simulado de orientación para trámites.",
                "address": "Sector Chapinero",
                "locality": "Chapinero",
                "latitude": 4.6469,
                "longitude": -74.0629,
                "phone": "6010000031",
                "website": "https://bia.local",
                "is_simulated": True,
            },
            {
                "name": "Servicio Ciudadano BIA Bosa",
                "category": "orientacion",
                "description": "Servicio ciudadano simulado.",
                "address": "Zona central de Bosa",
                "locality": "Bosa",
                "latitude": 4.6321,
                "longitude": -74.1948,
                "phone": "6010000032",
                "website": "https://bia.local",
                "is_simulated": True,
            },
            {
                "name": "Punto de Atención BIA Suba",
                "category": "atencion_ciudadana",
                "description": "Punto simulado de orientación ciudadana.",
                "address": "Centro de Suba",
                "locality": "Suba",
                "latitude": 4.7457,
                "longitude": -74.0942,
                "phone": "6010000033",
                "website": "https://bia.local",
                "is_simulated": True,
            },
            {
                "name": "Centro Ciudadano BIA Kennedy",
                "category": "tramites",
                "description": "Centro simulado de información y orientación.",
                "address": "Zona central de Kennedy",
                "locality": "Kennedy",
                "latitude": 4.6288,
                "longitude": -74.1608,
                "phone": "6010000034",
                "website": "https://bia.local",
                "is_simulated": True,
            },
        ]

        mobility = [
            {
                "type": "estacion",
                "name": "Estacion BIA Portal Norte",
                "description": "Estación de transporte simulada.",
                "status": "normal",
                "address": "Autopista Norte con Calle 170",
                "locality": "Suba",
                "latitude": 4.7565,
                "longitude": -74.0448,
                "is_simulated": True,
            },
            {
                "type": "estacion",
                "name": "Estacion BIA Centro",
                "description": "Estación de transporte simulada.",
                "status": "normal",
                "address": "Sector Centro",
                "locality": "La Candelaria",
                "latitude": 4.6012,
                "longitude": -74.0715,
                "is_simulated": True,
            },
            {
                "type": "corredor",
                "name": "Corredor BIA Avenida Caracas",
                "description": "Estado de corredor simulado.",
                "status": "congestionado",
                "address": "Avenida Caracas",
                "locality": "Chapinero",
                "latitude": 4.6404,
                "longitude": -74.0637,
                "is_simulated": True,
            },
            {
                "type": "estacion",
                "name": "Estacion BIA Kennedy",
                "description": "Estación de transporte simulada.",
                "status": "normal",
                "address": "Zona central de Kennedy",
                "locality": "Kennedy",
                "latitude": 4.6279,
                "longitude": -74.1628,
                "is_simulated": True,
            },
            {
                "type": "corredor",
                "name": "Corredor BIA Calle 80",
                "description": "Estado de corredor simulado.",
                "status": "fluido",
                "address": "Calle 80",
                "locality": "Barrios Unidos",
                "latitude": 4.6679,
                "longitude": -74.0821,
                "is_simulated": True,
            },
            {
                "type": "estacion",
                "name": "Estacion BIA Bosa",
                "description": "Estación de transporte simulada.",
                "status": "alerta",
                "address": "Zona central de Bosa",
                "locality": "Bosa",
                "latitude": 4.6289,
                "longitude": -74.1922,
                "is_simulated": True,
            },
        ]

        counters = {
            "events": 0,
            "health_services": 0,
            "places": 0,
            "city_services": 0,
            "mobility": 0,
        }

        for data in events:
            if add_event(db, data):
                counters["events"] += 1

        for data in health_services:
            if add_health_service(db, data):
                counters["health_services"] += 1

        for data in places:
            if add_place(db, data):
                counters["places"] += 1

        for data in city_services:
            if add_city_service(db, data):
                counters["city_services"] += 1

        for data in mobility:
            if add_mobility(db, data):
                counters["mobility"] += 1

        db.commit()

        print("Seed de BIA completado.")
        print(f"Eventos agregados: {counters['events']}")
        print(f"Servicios de salud agregados: {counters['health_services']}")
        print(f"Lugares agregados: {counters['places']}")
        print(f"Servicios ciudadanos agregados: {counters['city_services']}")
        print(f"Registros de movilidad agregados: {counters['mobility']}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
