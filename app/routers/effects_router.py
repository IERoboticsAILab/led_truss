from fastapi import APIRouter, Depends
from rpi_ws281x import Color

from app.models import (
    BitcoinRequest, GlowRequest, WaveRequest, ColorWipeRequest,
    ColorFadeRequest, SparkleRequest, RainbowRequest, RainbowCycleRequest,
    TheaterChaseRequest, RunningRequest, HeartRateRequest
)
from app.core.dependencies import get_truss_controller
from app.core.truss import truss # Type hint for dependency

router = APIRouter(prefix="/effects", tags=["Visual Effects"])

@router.post("/bitcoin")
def bitcoin(request: BitcoinRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the Bitcoin price monitoring effect."""
    truss_controller.bitcoin(request.duration, request.time_threshold_in_secs)
    return {"status": "success"}

@router.post("/glow")
def glow_effect(request: GlowRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the glow effect with specified parameters."""
    color = Color(request.color.r, request.color.g, request.color.b)
    truss_controller.glow(color, request.frames, request.wait_ms)
    return {"status": "success"}

@router.post("/wave")
def wave_effect(request: WaveRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the wave effect with specified parameters."""
    color = Color(request.color.r, request.color.g, request.color.b)
    truss_controller.wave(color, request.frames, request.cycles, request.speed, request.wait_ms)
    return {"status": "success"}

@router.post("/color-wipe")
def color_wipe_effect(request: ColorWipeRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the color wipe effect with specified parameters."""
    color = Color(request.color.r, request.color.g, request.color.b)
    truss_controller.color_wipe(color, request.wait_ms)
    return {"status": "success"}

@router.post("/color-fade")
def color_fade_effect(request: ColorFadeRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the color fade effect with specified parameters."""
    color_from = Color(request.color_from.r, request.color_from.g, request.color_from.b)
    color_to = Color(request.color_to.r, request.color_to.g, request.color_to.b)
    truss_controller.color_fade(color_from, color_to, request.wait_ms, request.steps)
    return {"status": "success"}

@router.post("/sparkle")
def sparkle_effect(request: SparkleRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the sparkle effect, single or multi-color."""
    if request.color is None:
        # Use default multicolor sparkle if no color is provided
        truss_controller.sparkle_multicolor(request.wait_ms, request.cummulative)
    else:
        # Use specified color
        color = Color(request.color.r, request.color.g, request.color.b)
        truss_controller.sparkle(color, request.wait_ms, request.cummulative)
    return {"status": "success"}

@router.post("/rainbow")
def rainbow_effect(request: RainbowRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the rainbow effect."""
    truss_controller.rainbow(request.wait_ms, request.iterations)
    return {"status": "success"}

@router.post("/rainbow-cycle")
def rainbow_cycle_effect(request: RainbowCycleRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the rainbow cycle effect."""
    truss_controller.rainbow_cycle(request.wait_ms, request.iterations)
    return {"status": "success"}

@router.post("/theater-chase")
def theater_chase_effect(request: TheaterChaseRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the theater chase effect, single color or rainbow."""
    if request.color is None:
        # Use default rainbow chase if no color is provided
        truss_controller.theater_chase_rainbow(request.wait_ms)
    else:
        # Use specified color
        color = Color(request.color.r, request.color.g, request.color.b)
        truss_controller.theater_chase(color, request.wait_ms, request.iterations)
    return {"status": "success"}

@router.post("/running")
def running_effect(request: RunningRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the running lights effect."""
    truss_controller.running(request.wait_ms, request.duration_ms, request.width)
    return {"status": "success"} 

@router.post("/heart-rate")
def heart_rate_effect(request: HeartRateRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Monitors a heart rate URL and displays color-coded status."""
    truss_controller.heart_rate(
        url=str(request.url),
        duration=request.duration,
        poll_interval_ms=request.poll_interval_ms,
        min_hr=request.min_hr,
        yellow_start=request.yellow_start,
        red_start=request.red_start,
        max_hr=request.max_hr,
    )
    return {"status": "success"}