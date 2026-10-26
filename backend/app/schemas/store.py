from pydantic import BaseModel, ConfigDict, EmailStr, Field

class StoreBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, examples=["Nike Factory Store"])
    category: str = Field(..., min_length=1, max_length=255, examples=["Apparel & Footwear"])
    hours: str | None = Field(default=None, max_length=255, examples=["Mon-Sat: 10am-9pm, Sun: 11am-7pm"])
    accessible: bool = Field(default=False, description="Wheelchair / accessibility compliance")
    zone: str = Field(..., min_length=1, max_length=20, examples=["Zone A"])
    amenities: list[str] = Field(default_factory=list, examples=[["wheelchair_accessible", "curbside_pickup"]])
    coordinates: list[float] = Field(..., min_length=2, max_length=2, examples=[[124.5, 340.2]])
  
class StoreCreate(BaseModel):
    id: str | None = Field(
        default = None 
    )

class StoreUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    category: str | None = Field(default=None, min_length=1, max_length=255)
    hours: str | None = Field(default=None, max_length=255)
    accessible: bool | None = Field(default=None)
    zone: str | None = Field(default=None, min_length=1, max_length=20)
    amenities: list[str] | None = Field(default=None)
    coordinates: list[float] | None = Field(default=None, min_length=2, max_length=2)

class StoreResponse(BaseModel):
    id: str = Field(...)
    model_config = ConfigDict(from_attributes=True)