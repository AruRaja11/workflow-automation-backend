from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    Boolean,
    DateTime,
    Identity,
    text
)
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text("TRUE")
    )