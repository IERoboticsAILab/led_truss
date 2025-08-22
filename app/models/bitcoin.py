from pydantic import BaseModel, Field
 
class BitcoinRequest(BaseModel):
    time_threshold_in_secs: int = Field(default=30, ge=1, description="How long to show each price change window") 