from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.services import user_service
from app.models.user import User, UserRole

# Annotated[Type, extra_info] means "This value has this type, and here's some additional information about it. 
# No need to repeatedly write "db: Session = Depends(get_db)".With Annotated, you define the dependency once and reuse it
SessionDep = Annotated[Session, Depends(get_db)]

bearer_scheme = HTTPBearer(auto_error= False)
BearerDep = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]

def get_current_user(db: SessionDep, credentials: BearerDep):
    if credentials is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Sign in to continue")
    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError as e:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid or expired token.")
    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id.strip():
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid user id")
    user = user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid user")
    return user

def require_operator(user: Annotated[User, Depends(get_current_user)]) -> None:
    if user.role.value != UserRole.OPERATOR:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Access restricted.")

def require_tenant(user: Annotated[User, Depends(get_current_user)]) -> User | None:
    if user.role.value != UserRole.TENANT:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Access restricted.")
    return user



