from pydantic import BaseModel, ConfigDict, Field


class DayHours(BaseModel):
    open: str | None = Field(default=None, examples=["10:00"])
    close: str | None = Field(default=None, examples=["21:00"])
    is_closed: bool = Field(default=False, examples=[False])


class StoreBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, examples=["Nike Factory Store"])
    category: str = Field(..., min_length=1, max_length=255, examples=["Apparel & Footwear"])
    hours: dict[str, DayHours] | None = Field(
        default=None,
        examples=[
            {
                "monday": {"open": "10:00", "close": "21:00", "is_closed": False},
                "tuesday": {"open": "10:00", "close": "21:00", "is_closed": False},
                "sunday": {"open": "11:00", "close": "18:00", "is_closed": False},
            }
        ],
    )
    accessible: bool = Field(default=False, description="Wheelchair / accessibility compliance")
    zone: str = Field(..., min_length=1, max_length=20, examples=["Zone A"])
    amenities: list[str] = Field(default_factory=list, examples=[["wheelchair_accessible", "curbside_pickup"]])
    coordinates: list[float] = Field(..., min_length=2, max_length=2, examples=[[124.5, 340.2]])


class StoreCreate(StoreBase):
    # create even if no id provided. will use uuid if no id provided
    id: str | None = Field(default=None)


class StoreUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    category: str | None = Field(default=None, min_length=1, max_length=255)
    hours: dict[str, DayHours] | None = Field(default=None)
    accessible: bool | None = Field(default=None)
    zone: str | None = Field(default=None, min_length=1, max_length=20)
    amenities: list[str] | None = Field(default=None)
    coordinates: list[float] | None = Field(default=None, min_length=2, max_length=2)


class StoreResponse(StoreBase):
    id: str = Field(...)
    model_config = ConfigDict(from_attributes=True)
