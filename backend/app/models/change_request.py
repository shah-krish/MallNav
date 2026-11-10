import enum
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class ChangeRequestStatus(str, enum. Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class StoreChangeRequest(Base):
    __tablename__ = "store_change_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    store_id: Mapped[str] = mapped_column(String(36), ForeignKey("stores.id", ondelete="CASCADE"), nullable= False, index= True)
    requested_by_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete= "CASCADE"), nullable= False)

    # dict[str, Any] = Type hint -> keys are strings and values can be anything. 
    proposed_changes: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable= False)
    status: Mapped[ChangeRequestStatus] = mapped_column(Enum(ChangeRequestStatus, native_enum= False), default= ChangeRequestStatus.PENDING, nullable= False, index= True)

    # Text: Longer text without a length limit
    review_notes: Mapped[str | None] = mapped_column(Text, nullable= True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable= False)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone= True), nullable= True)
    