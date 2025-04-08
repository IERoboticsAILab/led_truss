from typing import Union, Tuple, Optional
from fastapi import FastAPI
from rpi_ws281x import Color

import sys
sys.path.insert(0, '../lib')
from truss import truss

import time
import json 
import requests 

app = FastAPI()
truss = truss()
truss.set_brightness(255)
truss.glow(Color(255,255,255))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/bitcoin")
def bitcoin():
    # defining key/request url 
    key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR"
    
    # define a starting price
    previous_price = 0
    price_change_percentage = 0

    # define a time threshold (in secs)
    time_threshold_in_secs = 30 

    while True:
        # requesting data from url 
        data = requests.get(key) 
        data = data.json() 
        current_price = int(float(data['price']))
        timeout = time.time() + time_threshold_in_secs

        if previous_price is not 0:
            price_change_percentage = percentage_change(current_price,previous_price)

        truss.clear_all()

        if current_price > previous_price:
            while time.time() < timeout:
                truss.glow(Color(0,255,0))
        if current_price < previous_price:
            while time.time() < timeout:
                truss.glow(Color(255,0,0))
  
        previous_price = current_price
        time.sleep(1)
    return 0

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