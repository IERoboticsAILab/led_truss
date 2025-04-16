from pydantic import BaseModel, Field
 
class BitcoinRequest(BaseModel):
    duration: int = Field(default=60, ge=1, description="Total duration to monitor in seconds")
    time_threshold_in_secs: int = Field(default=30, ge=1, description="How long to show each price change") 