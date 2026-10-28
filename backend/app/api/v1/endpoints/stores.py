from fastapi import APIRouter, HTTPException, status
from app.api.deps import SessionDep
from app.schemas.store import StoreCreate, StoreResponse
from app.services import store_service

router = APIRouter()

@router.get("/", response_model=list[StoreResponse])
def read_stores(db: SessionDep, skip: int =0, limit: int = 100, category: str | None = None, zone: str | None = None):
   return store_service.get_stores(db, skip, limit, category, zone)

@router.get("/{id}", response_model=StoreResponse)
def read_store_by_id(db: SessionDep, id: str):
   store = store_service.get_store_by_id(db, id)
   if store is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Store with id: {id} not found")
   return store 