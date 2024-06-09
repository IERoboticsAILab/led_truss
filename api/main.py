from typing import Union
from fastapi import FastAPI

import sys
sys.path.insert(0, '../lib')
from truss import truss
from rpi_ws281x import Color

app = FastAPI()
truss = truss()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/mode/{mode_id}")
def read_mode(mode_id: int):
    if mode_id == 0:
        truss.glow(Color(0,255,0),10)
    return 0
