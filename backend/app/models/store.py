from sqlalchemy import DateTime, ForeignKey, Boolean, String, Text, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Store(Base):
    __tablename__ = "store"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    hours: Mapped[str] = mapped_column(String(255), nullable=True)
    accessible: Mapped[bool] = mapped_column(Boolean, default=False)
    zone: Mapped[str] = mapped_column(String(20), nullable=False)
    amenities: Mapped[list[String]] = mapped_column(JSON, nullable=False)
    coordinates: Mapped[list[Integer]] = mapped_column(JSON, nullable=False)


