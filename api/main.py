from typing import Union
from fastapi import FastAPI

import sys
sys.path.insert(0, '../lib')
from truss import truss
from rpi_ws281x import Color


import time
import json 
import requests 

app = FastAPI()
truss = truss()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/mode/{mode_id}")
def read_mode(mode_id: int, wait_ms: int):
    if mode_id == 0:
        truss.glow(Color(0,255,0), wait_ms)
    return 0

@app.get("/bitcoin")
def bitcoin():
    # defining key/request url 
    key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR"
    # define a starting price
    previous_price = 0

    while True:
        # requesting data from url 
        data = requests.get(key) 
        data = data.json() 

        if data['price'] >= previous_price:
            truss.glow(Color(0,255,0))
        else:
            truss.glow(Color(255,0,0))

        previous_price = data['price']
        time.sleep(10)

    return 0