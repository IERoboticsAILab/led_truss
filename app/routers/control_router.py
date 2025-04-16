"""API Router for direct LED control actions."""

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
    """Clears all LEDs (sets them to off/black)."""
    truss_controller.clear_all()
    return {"status": "success"}

@router.post("/set-color")
def set_color_all(request: SetColorRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Sets all LEDs to a specific color, or white if no color is provided."""
    if request.color is None:
        # Default to white if no color specified
        truss_controller.set_white_all()
    else:
        # Set to specified color
        color = Color(request.color.r, request.color.g, request.color.b)
        truss_controller.set_color_all(color)
    return {"status": "success"}

@router.post("/set-brightness")
def set_brightness(request: SetBrightnessRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Sets the overall brightness of the LED strips."""
    truss_controller.set_brightness(request.brightness)
    return {"status": "success"}

@router.post("/set-color-range-percent")
def set_color_range_percent(request: SetColorRangePercentRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Sets a specific color for a range of LEDs defined by percentages."""
    color = Color(request.color.r, request.color.g, request.color.b)
    truss_controller.set_color_range_percent(color, request.start_percent, request.end_percent)
    return {"status": "success"}

@router.post("/set-color-range-exact")
def set_color_range_exact(request: SetColorRangeExactRequest, truss_controller: truss = Depends(get_truss_controller)):
    """Sets a specific color for a range of LEDs defined by exact indices."""
    color = Color(request.color.r, request.color.g, request.color.b)
    truss_controller.set_color_range_exact(color, request.start_index, request.end_index)
    return {"status": "success"} 