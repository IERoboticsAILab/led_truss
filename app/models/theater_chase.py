from typing import Optional
from pydantic import BaseModel, Field
from .base import ColorTuple
 
class TheaterChaseRequest(BaseModel):
    color: Optional[ColorTuple] = None
    wait_ms: int = Field(default=50, ge=0, description="Delay between moves in milliseconds")
    iterations: int = Field(default=10, ge=1, description="Number of complete chase cycles") 