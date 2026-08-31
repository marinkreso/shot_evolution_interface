#!/usr/bin/env python3
import frontend
import landing
import on
import tec
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}

app.mount("/images", StaticFiles(directory="images"), name="images")



frontend.init(app)
landing.init(app)
on.init(app)
tec.init(app)