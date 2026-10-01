import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=True,
    )

    place_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("places.id", ondelete="CASCADE"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user = relationship(
        "User",
        back_populates="favorites",
    )

    event = relationship("Event")

    place = relationship("Place")

    __table_args__ = (
        CheckConstraint(
            "(event_id IS NOT NULL AND place_id IS NULL) "
            "OR (event_id IS NULL AND place_id IS NOT NULL)",
            name="ck_favorites_exactly_one_target",
        ),
        UniqueConstraint(
            "user_id",
            "event_id",
            name="uq_favorites_user_event",
        ),
        UniqueConstraint(
            "user_id",
            "place_id",
            name="uq_favorites_user_place",
        ),
    )
