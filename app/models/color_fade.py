from pydantic import BaseModel, Field
from .base import ColorTuple
 
class ColorFadeRequest(BaseModel):
    color_from: ColorTuple
    color_to: ColorTuple
    wait_ms: int = Field(default=20, ge=0, description="Delay between steps in milliseconds")
    steps: int = Field(default=100, ge=1, description="Number of color steps in the fade") 