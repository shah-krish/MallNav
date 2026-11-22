from fastapi import APIRouter, HTTPException, status, Depends
from app.api.deps import SessionDep, require_operator, require_tenant
from app.schemas.store import StoreCreate, StoreResponse, StoreUpdate
from app.services import store_service
from typing import Annotated
from app.models.user import User
from app.schemas.change_request import ChangeRequestCreate, ChangeRequestResponse

# Creates a router object and assigns it a variable router
router = APIRouter()

@router.get("/", response_model=list[StoreResponse])
def read_stores(
    db: SessionDep,
    skip: int = 0,
    limit: int = 100,
    name: str | None = None,
    category: str | None = None,
    accessible: bool | None = None,
    zone: str | None = None,
):
    return store_service.get_stores(
        db,
        skip=skip,
        limit=limit,
        name=name,
        category=category,
        accessible=accessible,
        zone=zone,
    )

@router.get("/{id}", response_model=StoreResponse)
def read_store_by_id(db: SessionDep, id: str):
    store = store_service.get_store_by_id(db, id)
    if store is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Store with id: {id} not found")
    return store 

# By default FastAPI returns response code 200 (OK) but 201 signals that new record was committed to db
@router.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_operator)])
def create_store(db: SessionDep, store_in: StoreCreate):
    return store_service.create_store(db, store_in)

@router.patch("/{id}", response_model=StoreResponse, dependencies=[Depends(require_operator)])
def update_store(db: SessionDep, id: str, store_in: StoreUpdate):
    store = store_service.get_store_by_id(db, id)
    if store is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Store with id: {id} not found")
    return store_service.update_store(db, store, store_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_operator)])
def delete_store(db: SessionDep, id: str):
    store = store_service.get_store_by_id(db, id)
    if store is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Store with id: {id} not found")
    return store_service.delete_store(db, store)

@router.post("/{store_id}/change-requests", status_code=status.HTTP_201_CREATED, response_model= ChangeRequestResponse)
def change_requests(db: SessionDep, store_id: str, tenant: Annotated[User, Depends(require_tenant)], proposal: ChangeRequestCreate):
    if store_id != tenant.store_id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Access forbidden.")
    return store_service.create_change_request(db, proposal, store_id, tenant.id)
