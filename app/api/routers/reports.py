from pathlib import Path
from uuid import UUID, uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.routers.auth import get_current_user
from app.models.report import Report
from app.models.report_image import ReportImage
from app.models.user import User
from app.schemas.report import (
    ReportCreate,
    ReportImageResponse,
    ReportResponse,
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

UPLOAD_DIR = Path("uploads") / "reports"
MAX_IMAGE_SIZE = 5 * 1024 * 1024

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def build_location(latitude: float, longitude: float):
    return from_shape(
        Point(longitude, latitude),
        srid=4326,
    )


def get_user_report(
    report_id: UUID,
    user: User,
    db: Session,
) -> Report:
    report = db.scalar(
        select(Report).where(
            Report.id == report_id,
            Report.user_id == user.id,
        )
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado",
        )

    return report


@router.post(
    "",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_report(
    payload: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    report = Report(
        user_id=current_user.id,
        category=payload.category,
        title=payload.title,
        description=payload.description,
        status="received",
        latitude=payload.latitude,
        longitude=payload.longitude,
        address=payload.address,
        location=build_location(
            payload.latitude,
            payload.longitude,
        ),
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


@router.get(
    "/me",
    response_model=list[ReportResponse],
)
def list_my_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = (
        select(Report)
        .where(Report.user_id == current_user.id)
        .order_by(Report.created_at.desc())
    )

    return db.scalars(query).all()


@router.get(
    "/{report_id}",
    response_model=ReportResponse,
)
def get_my_report(
    report_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_report(
        report_id=report_id,
        user=current_user,
        db=db,
    )


@router.post(
    "/{report_id}/images",
    response_model=ReportImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_report_image(
    report_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    report = get_user_report(
        report_id=report_id,
        user=current_user,
        db=db,
    )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Solo se permiten imágenes JPG, PNG o WEBP",
        )

    extension = ALLOWED_CONTENT_TYPES[file.content_type]
    file_id = uuid4()

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = UPLOAD_DIR / f"{file_id}{extension}"

    contents = await file.read(MAX_IMAGE_SIZE + 1)

    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="La imagen supera el límite de 5 MB",
        )

    file_path.write_bytes(contents)

    image = ReportImage(
        report_id=report.id,
        file_path=str(file_path).replace("\\", "/"),
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return image
