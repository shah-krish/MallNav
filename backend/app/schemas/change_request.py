from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from app.models.change_request import ChangeRequestStatus

class ChangeRequestCreate(BaseModel):
    proposed_changes: dict[str, Any] = Field(..., examples=[{"hours": {"monday": {"open": "09:00", "close": "20:00", "is_closed": False}}}])

class ChangeRequestReview(BaseModel):
    review_notes: str | None = Field(default=None, examples=["Approved updated weekday hours"])

class ChangeRequestResponse(BaseModel):
    id: str
    store_id: str
    requested_by_user_id: str
    proposed_changes: dict[str, Any]
    status: ChangeRequestStatus
    review_notes: str | None = None
    created_at: datetime
    reviewed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


