from pydantic import BaseModel, Field

class RainbowRequest(BaseModel):
    wait_ms: int = Field(default=50, ge=0, description="Delay between updates in milliseconds")
    iterations: int = Field(default=1, ge=1, description="Number of complete rainbow cycles")
 
class RainbowCycleRequest(BaseModel):
    wait_ms: int = Field(default=50, ge=0, description="Delay between updates in milliseconds")
    iterations: int = Field(default=5, ge=1, description="Number of complete rainbow cycles") 