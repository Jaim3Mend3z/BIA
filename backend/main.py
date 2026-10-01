from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine, test_database_connection


app = FastAPI(
    title="BIA API",
    description="API de Bogotá Inteligente Asistente",
    version="0.2.0"
)


@app.get("/")
def root():
    return {
        "name": "BIA",
        "description": "Bogotá Inteligente Asistente",
        "version": "0.2.0",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/health/database")
def health_database():
    version = test_database_connection()

    return {
        "status": "healthy",
        "database": "connected",
        "postgresql_version": version
    }


@app.get("/health/postgis")
def health_postgis():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT PostGIS_Version();")
        )
        version = result.scalar()

    return {
        "status": "healthy",
        "postgis": "connected",
        "postgis_version": version
    }
