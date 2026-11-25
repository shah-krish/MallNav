from fastapi import APIRouter, Depends

from app.api.deps import SessionDep, require_operator
from app.schemas.change_request import ChangeRequestResponse, ChangeRequestReview
from app.services import change_request_service, store_service


router = APIRouter()

@router.get('/pending', response_model= list[ChangeRequestResponse], dependencies= [Depends(require_operator)])
def list_pending_change_requests(db: SessionDep):
    return store_service.list_pending_change_requests(db)

@router.post("/{request_id}/reject", response_model=ChangeRequestResponse, dependencies=[Depends(require_operator)])
def reject_pending_request(db: SessionDep, request_id: str, review: ChangeRequestReview):
    return change_request_service.reject_change_request(db, request_id, review.review_notes)
