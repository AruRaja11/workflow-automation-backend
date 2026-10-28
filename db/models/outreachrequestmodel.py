import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Numeric,
    Sequence,
    Text,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from db.models.base import Base



class ClOutreachRequest(Base):
    __tablename__ = "cl_outreach_requests"

    __table_args__ = (
        CheckConstraint(
            "search_place_count >= 0",
            name="chk_search_place_count",
        ),
    )

    seq_id: Mapped[int] = mapped_column(
        BigInteger,
        Sequence("seq_cl_outreach_requests"),
        nullable=False,
        unique=True,
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    business1: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    business2: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    business3: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    pitch: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    search_place_count: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        server_default=text("3"),
    )

    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    request_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        server_default=text("'pending'"),
    )

    message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
