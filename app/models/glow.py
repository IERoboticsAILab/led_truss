from pydantic import BaseModel, Field
from .base import ColorTuple
 
class GlowRequest(BaseModel):
    color: ColorTuple
    wait_ms: int = Field(default=10, ge=0, description="Delay between frames in milliseconds") 