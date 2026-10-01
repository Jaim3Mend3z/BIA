from fastapi import FastAPI

from app.api.routers import auth, health

app = FastAPI(
    title="BIA - Bogotá Inteligente Asistente",
    description="API principal de la plataforma BIA.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(auth.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "name": "BIA",
        "description": "Bogotá Inteligente Asistente",
        "status": "running",
        "version": "0.1.0",
    }
