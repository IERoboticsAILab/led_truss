from typing import Union
from fastapi import FastAPI

import sys

sys.path.insert(0, '/root/led_truss/')
import main

import time
import math
from rpi_ws281x import *

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/mode/{mode_id}")
def read_mode(mode_id: int):

    if mode_id == 0:
        main.rainbow()
    if mode_id == 1:
        color = Color(0,0,255)
        main.glow(color,0.01)

    return 0
