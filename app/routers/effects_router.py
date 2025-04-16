from fastapi import APIRouter, Depends
from rpi_ws281x import Color

from app.models import (
    BitcoinRequest, GlowRequest, WaveRequest, ColorWipeRequest,
    ColorFadeRequest, SparkleRequest, RainbowRequest, RainbowCycleRequest,
    TheaterChaseRequest, RunningRequest
)
from app.core.dependencies import get_truss_controller
from app.core.truss import truss # Type hint for dependency
from app.effects import get_effects

router = APIRouter(prefix="/effects", tags=["Visual Effects"])

@router.post("/bitcoin")
def bitcoin(request: BitcoinRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: bitcoin --- Request: {request}")
    # truss_controller.bitcoin(request.duration, request.time_threshold_in_secs)
    return {"status": "success"}

@router.post("/glow")
def glow_effect(request: GlowRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: glow --- Request: {request}")
    color = Color(request.color.r, request.color.g, request.color.b)
    # truss_controller.glow(color, request.frames, request.wait_ms)
    return {"status": "success"}

@router.post("/wave")
def wave_effect(request: WaveRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: wave --- Request: {request}")
    color = Color(request.color.r, request.color.g, request.color.b)
    # truss_controller.wave(color, request.frames, request.cycles, request.speed, request.wait_ms)
    return {"status": "success"}

@router.post("/color-wipe")
def color_wipe_effect(request: ColorWipeRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: color_wipe --- Request: {request}")
    color = Color(request.color.r, request.color.g, request.color.b)
    # truss_controller.color_wipe(color, request.wait_ms)
    return {"status": "success"}

@router.post("/color-fade")
def color_fade_effect(request: ColorFadeRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: color_fade --- Request: {request}")
    color_from = Color(request.color_from.r, request.color_from.g, request.color_from.b)
    color_to = Color(request.color_to.r, request.color_to.g, request.color_to.b)
    # truss_controller.color_fade(color_from, color_to, request.wait_ms, request.steps)
    return {"status": "success"}

@router.post("/sparkle")
def sparkle_effect(request: SparkleRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: sparkle --- Request: {request}")
    if request.color is None:
        # truss_controller.sparkle_multicolor(request.wait_ms, request.cummulative)
        pass # Added pass since the call was commented out
    else:
        color = Color(request.color.r, request.color.g, request.color.b)
        # truss_controller.sparkle(color, request.wait_ms, request.cummulative)
    return {"status": "success"}

@router.post("/rainbow")
def rainbow_effect(request: RainbowRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: rainbow --- Request: {request}")
    # truss_controller.rainbow(request.wait_ms, request.iterations)
    return {"status": "success"}

@router.post("/rainbow-cycle")
def rainbow_cycle_effect(request: RainbowCycleRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: rainbow_cycle --- Request: {request}")
    # truss_controller.rainbow_cycle(request.wait_ms, request.iterations)
    return {"status": "success"}

@router.post("/theater-chase")
def theater_chase_effect(request: TheaterChaseRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: theater_chase --- Request: {request}")
    if request.color is None:
        # truss_controller.theater_chase_rainbow(request.wait_ms)
        pass # Added pass since the call was commented out
    else:
        color = Color(request.color.r, request.color.g, request.color.b)
        # truss_controller.theater_chase(color, request.wait_ms, request.iterations)
    return {"status": "success"}

@router.post("/running")
def running_effect(request: RunningRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: running --- Request: {request}")
    # truss_controller.running(request.wait_ms, request.duration_ms, request.width)
    return {"status": "success"} 