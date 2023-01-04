from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Union
from pathlib import Path
from app.models import mongodb
from app.models.book import Book


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI()
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    book = Book(keyword="파이썬", publisher="duan", price=10000, image='test')
    await mongodb.engine.save(book)
    return templates.TemplateResponse("./index.html", {"request": request, "title": "북북이"})


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    print(q)
    return templates.TemplateResponse("./index.html", {"request": request, "title": "서치", "keyword": q})


@app.on_event("startup")
def on_app_start():
    """before app starts"""
    print("hello")
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    """after app shutdown"""
    mongodb.close()
