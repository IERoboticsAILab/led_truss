from typing import Union
from fastapi import FastAPI

import sys
from ..lib import main

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
        truss.rainbow()
    return 0
