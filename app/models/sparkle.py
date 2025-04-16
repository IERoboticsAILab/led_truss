from typing import Optional
from pydantic import BaseModel, Field
from .base import ColorTuple
 
class SparkleRequest(BaseModel):
    color: Optional[ColorTuple] = None
    wait_ms: int = Field(default=50, ge=0, description="Delay between sparkles in milliseconds")
    cummulative: bool = Field(default=False, description="Whether sparkles accumulate or clear between iterations") 