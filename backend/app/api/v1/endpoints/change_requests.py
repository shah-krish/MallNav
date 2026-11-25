from fastapi import APIRouter, Depends
from app.schemas.change_request import ChangeRequestResponse
from app.services import store_service
from app.api.deps import SessionDep, require_operator

router = APIRouter()

@router.get('/pending', response_model= list[ChangeRequestResponse], dependencies= [Depends(require_operator)])
def list_pending_change_requests(db: SessionDep):
    return store_service.list_pending_change_requests(db)