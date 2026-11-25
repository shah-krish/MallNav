from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.change_request import ChangeRequestStatus, StoreChangeRequest


def get_request_for_update(db: Session, request_id: str) -> StoreChangeRequest | None:
    stmt = (
        select(StoreChangeRequest)
        .where(StoreChangeRequest.id == request_id)
        .with_for_update()
    )
    return db.execute(stmt).scalar_one_or_none()


def reject_change_request(
    db: Session, request_id: str, review_notes: str | None
) -> StoreChangeRequest:
    request = get_request_for_update(db, request_id)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found.",
        )
    if request.status != ChangeRequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Request already reviewed.",
        )

    request.status = ChangeRequestStatus.REJECTED
    request.review_notes = review_notes
    request.reviewed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(request)
    return request
