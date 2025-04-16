from typing import Optional
from pydantic import BaseModel, Field
from .base import ColorTuple

class SetColorRequest(BaseModel):
    color: Optional[ColorTuple] = None

class SetBrightnessRequest(BaseModel):
    brightness: int = Field(default=125, ge=0, le=255, description="Brightness value (0-255)")

class SetColorRangePercentRequest(BaseModel):
    color: ColorTuple
    start_percent: float = Field(default=0.0, ge=0.0, le=1.0, description="Starting position as percentage (0.0-1.0)")
    end_percent: float = Field(default=1.0, ge=0.0, le=1.0, description="Ending position as percentage (0.0-1.0)")

class SetColorRangeExactRequest(BaseModel):
    color: ColorTuple
    start_index: int = Field(default=0, ge=0, lt=1800, description="Starting LED index")
    end_index: int = Field(default=1800, gt=0, le=1800, description="Ending LED index") 