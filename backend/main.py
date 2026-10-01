from fastapi import FastAPI

from app.api.routers import (
    auth,
    city_services,
    events,
    health,
    health_services,
    places,
)

app = FastAPI(
    title="BIA - Bogotá Inteligente Asistente",
    description="API principal de la plataforma BIA.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(health_services.router)
app.include_router(places.router)
app.include_router(city_services.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "name": "BIA",
        "description": "Bogotá Inteligente Asistente",
        "status": "running",
        "version": "0.1.0",
    }
