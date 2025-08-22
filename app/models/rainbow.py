from pydantic import BaseModel, Field

class RainbowRequest(BaseModel):
    wait_ms: int = Field(default=50, ge=0, description="Delay between updates in milliseconds")
 
class RainbowCycleRequest(BaseModel):
    wait_ms: int = Field(default=50, ge=0, description="Delay between updates in milliseconds")