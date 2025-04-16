from pydantic import BaseModel, Field
from .base import ColorTuple
 
class GlowRequest(BaseModel):
    color: ColorTuple
    frames: int = Field(default=300, ge=1, description="Number of animation frames")
    wait_ms: int = Field(default=10, ge=0, description="Delay between frames in milliseconds") 