from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Union
from pathlib import Path
from app.models import mongodb
from app.models.book import Book
from app.book_scraper import NaverBookScraper


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI()
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # book = Book(keyword="파이썬", publisher="duan", price=10000, image='test')
    # await mongodb.engine.save(book)
    return templates.TemplateResponse("./index.html", {"request": request, "title": "북북이"})


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    keyword = q
    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(keyword, 20)
    book_models = []
    for book in books:
        book_model = Book(
            keyword=keyword,
            publisher=book["publisher"],
            price=book["discount"],
            image=book["image"]
        )
        book_models.append(book_model)
    await mongodb.engine.save_all(book_models)
    return templates.TemplateResponse("./index.html", {"request": request, "title": "긴긴주안", "keyword": q, "books": books})


@app.on_event("startup")
def on_app_start():
    """before app starts"""
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    """after app shutdown"""
    mongodb.close()
