from sqlalchemy import Boolean, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    hours: Mapped[str | None] = mapped_column(String(255), nullable=True)
    accessible: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    zone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    amenities: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    coordinates: Mapped[list[float]] = mapped_column(JSON, nullable=False)

