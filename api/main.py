from typing import Union, Tuple, Optional
from fastapi import FastAPI
from rpi_ws281x import Color

import sys
sys.path.insert(0, '../lib')
from lib.truss import truss

app = FastAPI()
truss = truss()
truss.clear_all()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/bitcoin")
def bitcoin(duration: int = 60, time_threshold_in_secs: int = 30):
    truss.bitcoin(duration, time_threshold_in_secs)
    return {"status": "success"}
# Visualization Effects Endpoints
@app.get("/glow")
def glow_effect(color: Tuple[int, int, int] = (255, 255, 255), frames: int = 300, wait_ms: int = 10):
    truss.glow(Color(*color), frames, wait_ms)
    return {"status": "success"}

@app.get("/wave")
def wave_effect(color: Tuple[int, int, int] = (255, 255, 255), frames: int = 300, cycles: int = 1, speed: float = 0.1, wait_ms: int = 10):
    truss.wave(Color(*color), frames, cycles, speed, wait_ms)
    return {"status": "success"}

@app.get("/color-wipe")
def color_wipe_effect(color: Tuple[int, int, int] = (255, 255, 255), wait_ms: int = 50):
    truss.color_wipe(Color(*color), wait_ms)
    return {"status": "success"}

@app.get("/color-fade")
def color_fade_effect(color_from: Tuple[int, int, int] = (0, 0, 0), 
                     color_to: Tuple[int, int, int] = (255, 255, 255),
                     wait_ms: int = 20, steps: int = 100):
    truss.color_fade(Color(*color_from), Color(*color_to), wait_ms, steps)
    return {"status": "success"}

@app.get("/sparkle")
def sparkle_effect(color: Optional[Tuple[int, int, int]] = None, wait_ms: int = 50, cummulative: bool = False):
    if color is None:
        truss.sparkle_multicolor(wait_ms, cummulative)
    else:
        truss.sparkle(Color(*color), wait_ms, cummulative)
    return {"status": "success"}

@app.get("/rainbow")
def rainbow_effect(wait_ms: int = 50, iterations: int = 1):
    truss.rainbow(wait_ms, iterations)
    return {"status": "success"}

@app.get("/rainbow-cycle")
def rainbow_cycle_effect(wait_ms: int = 50, iterations: int = 5):
    truss.rainbow_cycle(wait_ms, iterations)
    return {"status": "success"}

@app.get("/theater-chase")
def theater_chase_effect(color: Optional[Tuple[int, int, int]] = None, wait_ms: int = 50, iterations: int = 10):
    if color is None:
        truss.theater_chase_rainbow(wait_ms)
    else:
        truss.theater_chase(Color(*color), wait_ms, iterations)
    return {"status": "success"}

@app.get("/running")
def running_effect(wait_ms: int = 10, duration_ms: int = 18000, width: int = 1):
    truss.running(wait_ms, duration_ms, width)
    return {"status": "success"}

@app.get("/clear")
def clear_all():
    truss.clear_all()
    return {"status": "success"}

@app.get("/set-color")
def set_color_all(color: Tuple[int, int, int] = (255, 255, 255)):
    truss.set_color_all(Color(*color))
    return {"status": "success"}

@app.get("/set-white")
def set_white_all():
    truss.set_white_all()
    return {"status": "success"}

@app.get("/set-brightness")
def set_brightness(brightness: int = 125):
    truss.set_brightness(brightness)
    return {"status": "success"}

@app.get("/set-color-range-percent")
def set_color_range_percent(color: Tuple[int, int, int] = (255, 255, 255), start_percent: float = 0.0, end_percent: float = 1.0):
    truss.set_color_range_percent(Color(*color), start_percent, end_percent)
    return {"status": "success"}

@app.get("/set-color-range-exact")
def set_color_range_exact(color: Tuple[int, int, int] = (255, 255, 255), start_index: int = 0, end_index: int = 1800):
    truss.set_color_range_exact(Color(*color), start_index, end_index)
    return {"status": "success"}
