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
    truss_controller.start_effect("bitcoin", request.time_threshold_in_secs, clear_first=True)
    return {"status": "success"}

@router.post("/glow")
def glow_effect(request: GlowRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the glow effect with specified parameters."""
    color = Color(request.color.r, request.color.g, request.color.b)
    truss_controller.start_effect("glow", color, request.wait_ms, clear_first=True)
    return {"status": "success"}

@router.post("/wave")
def wave_effect(request: WaveRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the wave effect with specified parameters."""
    color = Color(request.color.r, request.color.g, request.color.b)
    truss_controller.start_effect("wave", color, request.cycles, request.speed, request.wait_ms, clear_first=True)
    return {"status": "success"}

@router.post("/color-wipe")
def color_wipe_effect(request: ColorWipeRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the color wipe effect with specified parameters."""
    color = Color(request.color.r, request.color.g, request.color.b)
    truss_controller.start_effect("color_wipe", color, request.wait_ms, clear_first=True)
    return {"status": "success"}

@router.post("/color-fade")
def color_fade_effect(request: ColorFadeRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the color fade effect with specified parameters."""
    color_from = Color(request.color_from.r, request.color_from.g, request.color_from.b)
    color_to = Color(request.color_to.r, request.color_to.g, request.color_to.b)
    truss_controller.start_effect("color_fade", color_from, color_to, request.wait_ms, request.steps, clear_first=True)
    return {"status": "success"}

@router.post("/sparkle")
def sparkle_effect(request: SparkleRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the sparkle effect, single or multi-color."""
    if request.color is None:
        truss_controller.start_effect("sparkle_multicolor", request.wait_ms, request.cummulative, clear_first=True)
    else:
        color = Color(request.color.r, request.color.g, request.color.b)
        truss_controller.start_effect("sparkle", color, request.wait_ms, request.cummulative, clear_first=True)
    return {"status": "success"}

@router.post("/rainbow")
def rainbow_effect(request: RainbowRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the rainbow effect."""
    truss_controller.start_effect("rainbow", request.wait_ms, clear_first=True)
    return {"status": "success"}

@router.post("/rainbow-cycle")
def rainbow_cycle_effect(request: RainbowCycleRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the rainbow cycle effect."""
    truss_controller.start_effect("rainbow_cycle", request.wait_ms, clear_first=True)
    return {"status": "success"}

@router.post("/theater-chase")
def theater_chase_effect(request: TheaterChaseRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the theater chase effect, single color or rainbow."""
    if request.color is None:
        truss_controller.start_effect("theater_chase_rainbow", request.wait_ms, clear_first=True)
    else:
        color = Color(request.color.r, request.color.g, request.color.b)
        truss_controller.start_effect("theater_chase", color, request.wait_ms, clear_first=True)
    return {"status": "success"}

@router.post("/running")
def running_effect(request: RunningRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Triggers the running lights effect."""
    truss_controller.start_effect("running", request.wait_ms, request.width, clear_first=True)
    return {"status": "success"} 

@router.post("/heart-rate")
def heart_rate_effect(request: HeartRateRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Monitors a heart rate URL and displays color-coded status."""
    truss_controller.start_effect(
        "heart_rate",
        str(request.url),
        request.poll_interval,
        request.min_hr,
        request.yellow_start,
        request.red_start,
        request.max_hr,
        clear_first=True,
    )
    return {"status": "success"}