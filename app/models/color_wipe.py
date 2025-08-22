from pydantic import BaseModel, Field
from .base import ColorTuple
 
class ColorWipeRequest(BaseModel):
    color: ColorTuple
    wait_ms: int = Field(default=50, ge=0, description="Delay between pixels in milliseconds") 