from pydantic import BaseModel, Field


class HeartRateRequest(BaseModel):
    url: str = Field(..., description="Endpoint returning the current heart rate (JSON or plain number)")
    duration: int = Field(default=300, ge=1, description="Total duration to monitor in seconds")
    poll_interval: float = Field(default=1.0, gt=0, description="How often to poll the URL in hertz (times per second)")
    min_hr: int = Field(default=40, ge=0, description="Lower bound for green start")
    yellow_start: int = Field(default=75, ge=0, description="Threshold where green transitions to yellow")
    red_start: int = Field(default=120, ge=0, description="Threshold where yellow transitions to red")
    max_hr: int = Field(default=200, ge=1, description="Upper bound for clamping and full red")

