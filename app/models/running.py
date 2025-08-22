from pydantic import BaseModel, Field
 
class RunningRequest(BaseModel):
    wait_ms: int = Field(default=10, ge=0, description="Delay between moves in milliseconds")
    width: int = Field(default=1, ge=1, description="Width of the running light in pixels") 