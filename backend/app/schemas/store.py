from pydantic import BaseModel, ConfigDict, EmailStr, Field

class StoreBase(BaseModel):
    id: str = Field(min_length=1, max_length=36)
  
