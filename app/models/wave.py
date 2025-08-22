from pydantic import BaseModel, Field
from .base import ColorTuple

class WaveRequest(BaseModel):
    color: ColorTuple
    cycles: int = Field(default=1, ge=1, description="Number of wave cycles along the strip")
    speed: float = Field(default=0.1, gt=0, description="Wave movement speed")
    wait_ms: int = Field(default=10, ge=0, description="Delay between frames in milliseconds") 