from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.database import test_database_connection

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health():
    return {
        "status": "healthy",
        "service": "bia-api",
    }


@router.get("/database")
def health_database():
    version = test_database_connection()

    return {
        "status": "healthy",
        "database": "connected",
        "postgresql_version": version,
    }


@router.get("/database-session")
def health_database_session(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    value = result.scalar_one()

    return {
        "status": "healthy",
        "database_session": "working",
        "test_query": value,
    }
