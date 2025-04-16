from fastapi import APIRouter, Depends
from rpi_ws281x import Color

from app.models import (
    SetColorRequest, SetBrightnessRequest,
    SetColorRangePercentRequest, SetColorRangeExactRequest
)
from app.core.dependencies import get_truss_controller
from app.core.truss import truss # Type hint for dependency

router = APIRouter(prefix="/control", tags=["Direct Control"])

@router.post("/clear")
def clear_all(truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: clear ---")
    truss_controller.clear_all()
    return {"status": "success"}

@router.post("/set-color")
def set_color_all(request: SetColorRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: set_color --- Request: {request}")
    if request.color is None:
        truss_controller.set_white_all()
    else:
        color = Color(request.color.r, request.color.g, request.color.b)
        truss_controller.set_color_all(color)
    return {"status": "success"}

@router.post("/set-brightness")
def set_brightness(request: SetBrightnessRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: set_brightness --- Request: {request}")
    truss_controller.set_brightness(request.brightness)
    return {"status": "success"}

@router.post("/set-color-range-percent")
def set_color_range_percent(request: SetColorRangePercentRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: set_color_range_percent --- Request: {request}")
    color = Color(request.color.r, request.color.g, request.color.b)
    truss_controller.set_color_range_percent(color, request.start_percent, request.end_percent)
    return {"status": "success"}

@router.post("/set-color-range-exact")
def set_color_range_exact(request: SetColorRangeExactRequest, truss_controller: truss = Depends(get_truss_controller)):
    print(f"--- Endpoint: set_color_range_exact --- Request: {request}")
    color = Color(request.color.r, request.color.g, request.color.b)
    truss_controller.set_color_range_exact(color, request.start_index, request.end_index)
    return {"status": "success"} 