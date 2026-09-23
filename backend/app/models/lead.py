from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Integer,
    SmallInteger,
    String,
    Text,
    Uuid,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    __table_args__ = (
        CheckConstraint(
            "source IN ("
            "'website', "
            "'form', "
            "'api', "
            "'facebook_ads', "
            "'extension', "
            "'playwright', "
            "'manual'"
            ")",
            name="source_value",
        ),
        CheckConstraint(
            "score IS NULL OR score BETWEEN 0 AND 100",
            name="score_range",
        ),
        CheckConstraint(
            "temperature IS NULL "
            "OR temperature IN ('hot', 'warm', 'cold')",
            name="temperature_value",
        ),
        CheckConstraint(
            "occurrence_count >= 1",
            name="occurrence_count_positive",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(254),
        nullable=False,
        unique=True,
        index=True,
    )

    company: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    role: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(2048),
        nullable=True,
    )

    source: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="validated",
        server_default=text("'validated'"),
    )

    workflow_execution_id: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    score: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
    )

    temperature: Mapped[str | None] = mapped_column(
        String(8),
        nullable=True,
    )

    occurrence_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        server_default=text("1"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    last_received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
