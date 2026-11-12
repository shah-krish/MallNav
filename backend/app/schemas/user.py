from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from app.models.user import UserRole

class UserLogin(BaseModel):
    email: str = Field(..., examples=["tenant@mallnav.com"])
    password: str = Field(..., min_length= 4)

class UserCreate(BaseModel):
    email: str
    password: str
    role: UserRole
    store_id: str | None = None

class UserResponse(BaseModel):
    id: str
    email: str
    role: UserRole
    store_id: str | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes= True)

class Token(BaseModel):
    access_token: str

    # bearer means whoever has the valid token can use it to access protected endpoint
    token_type: str = "bearer"
    user: UserResponse

class TokenPayload(BaseModel):
    # sub: subject -> who token belongs to
    sub: str | None = None
    email: str | None = None
    role: str | None = None
    store_id: str | None = None