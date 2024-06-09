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

def percentage_change(previous, current):
    try:
        percentage = abs(previous - current)/((previous + current)/2) * 100
    except ZeroDivisionError:
        percentage = float('inf')
    return percentage

@app.get("/bitcoin")
def bitcoin():
    # defining key/request url 
    key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR"
    
    # define a starting price
    previous_price = 0
    price_change_percentage = 0

    # define a time threshold
    time_threshold_in_secs = 10 

    while True:
        # requesting data from url 
        data = requests.get(key) 
        data = data.json() 
        current_price = int(float(data['price']))
        timeout = time.time() + time_threshold_in_secs

        if previous_price is not 0:
            price_change_percentage = percentage_change(current_price,previous_price)

        truss.clear_all()

        if current_price >= previous_price:
            while time.time() < timeout:
                truss.glow(Color(0,255,0), 10)
        else:
            while time.time() < timeout:
                truss.glow(Color(255,0,0), 10)

        previous_price = current_price
        time.sleep(time_threshold_in_secs)

    return 0