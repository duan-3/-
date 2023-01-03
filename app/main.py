from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Union

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


app = FastAPI()
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "북북이"})
