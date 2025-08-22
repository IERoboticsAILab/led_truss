from pydantic import BaseModel, Field


class HeartRateRequest(BaseModel):
    url: str = Field(..., description="One or more heart rate URLs (comma-separated) exposing a .heartrate element")
    poll_interval: float = Field(default=1.0, gt=0, description="How often to poll the URL in hertz (times per second)")
    min_hr: int = Field(default=40, ge=0, description="Lower bound for green start")
    yellow_start: int = Field(default=75, ge=0, description="Threshold where green transitions to yellow")
    red_start: int = Field(default=120, ge=0, description="Threshold where yellow transitions to red")
    max_hr: int = Field(default=200, ge=1, description="Upper bound for clamping and full red")
    pulse: bool = Field(default=True, description="Whether LEDs should pulse at the current heart rate")

