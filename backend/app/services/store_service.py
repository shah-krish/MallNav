import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.store import Store
from app.schemas.store import StoreCreate

def get_store_by_id(db: Session, store_id: str)-> Store | None: 
    stmt = select(Store).where(Store.id == store_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()

def get_stores(db: Session, skip: int = 0, limit: int = 100, category: str | None = None, zone: str | None = None):
    stmt = select(Store)
    if category:
        stmt = stmt.where(Store.category == category)
    if zone:
        stmt = stmt.where(Store.zone == zone)
    stmt = stmt.offset(skip).limit(limit)
    result = db.execute(stmt)

    return list(result.scalars().all())

def create_store(db: Session, store_in: StoreCreate) -> Store:
    store_data = store_in.model_dump()

    if not store_data.get("id"):
        store_data["id"] = str(uuid.uuid4())

    store = Store(**store_data) #unpack dictionary into our model

    db.add(store)
    db.commit()
    db.refresh(store)
    return store