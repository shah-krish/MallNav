import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, user_email: str) -> User | None:
    stmt = select(User).where(User.email == user_email)
    result = db.execute(stmt)
    return result.scalar_one_or_none()

def get_user_by_id(db: Session, user_id: str) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()

def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(
        id = str(uuid.uuid4()),
        email = user_in.email,
        hashed_password = get_password_hash(user_in.password),
        role = user_in.role,
        store_id = user_in.store_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if verify_password(password, user.hashed_password):
        return user
    else:
        return None