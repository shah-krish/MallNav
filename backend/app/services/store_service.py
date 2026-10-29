import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.store import Store
from app.schemas.store import StoreCreate, StoreUpdate


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

# store_in: StoreCreate = FastAPI reads incoming JSON, validates against StoreCreate model (Pydantic), and creates a StoreCreate object
def create_store(db: Session, store_in: StoreCreate) -> Store:
    store_data = store_in.model_dump() 

    if not store_data.get("id"):
        store_data["id"] = str(uuid.uuid4())

    store = Store(**store_data) #unpack dictionary into our model

    db.add(store)
    db.commit()
    db.refresh(store)
    return store

def update_store(db: Session, store: Store, store_in: StoreUpdate) -> Store:
    # Extract only fields that are sent in the request
    store_data = store_in.model_dump(exclude_unset=True)
    for field, value in store_data.items():
        setattr(store, field, value)
    db.commit()
    db.refresh(store)
    return store

def delete_store(db: Session, store: Store) -> None:
    db.delete(store)
    db.commit()
    
