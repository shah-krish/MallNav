from fastapi import APIRouter, HTTPException, status
from app.api.deps import SessionDep
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.core.security import create_access_token
from app.services import user_service
from app.models.user import User, UserRole

router = APIRouter()

# @router.post("/register", response_model= UserResponse, status_code = status.HTTP_201_CREATED)
def register_user(db: SessionDep, user_in: UserCreate) -> User | None :
    if user_service.get_user_by_email(db, user_in.email) is not None: 
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "A user with this email already exists. Please login with this email id.")
    return user_service.create_user(db, user_in)

@router.post("/login", response_model= Token)
def login_user(db: SessionDep, user_in: UserLogin):
    user = user_service.authenticate_user(db, user_in.email, user_in.password) 
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Incorrect email or password.")

    if not (user.role.value == UserRole.OPERATOR or user.role.value == UserRole.TENANT):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Forbidden access.") 
    
    user_data = {
        "sub": user.id,
        "role": user.role.value,
        "store_id": user.store_id
    }
    token = create_access_token(user_data)
    return Token(access_token= token, token_type= "bearer", user= UserResponse.model_validate(user))
