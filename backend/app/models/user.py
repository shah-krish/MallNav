from typing import Any
from sqlalchemy import Enum, String, ForeignKey, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
import enum
from app.db.base import Base

class UserRole(str, enum.Enum):
    VISITOR = "VISITOR"
    TENANT = "TENANT"
    OPERATOR = "OPERATOR"


class User(Base):
    __tablename__  = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    # index=True: Creates an index to make searching by email faster.
    email: Mapped[str] = mapped_column(String(255), unique= True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # native_enum=False: Store enum as a string in db instead of enum itself in db
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, native_enum = False), default=UserRole.VISITOR, nullable= False)

    # ForeignKey("stores.id"): store_id references the id column in the stores table. ondelete="SET NULL": Sets the foreign key to NULL when the referenced store is deleted.
    store_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("stores.id", ondelete="SET NULL"), nullable= True)

    # default=lambda: datetime.now(timezone.utc): automatically assigns the current UTC time when a new record is created. 
    # Without lambda: Python calculates the time when the model is loaded.
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable= False)
