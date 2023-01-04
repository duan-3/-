import asyncio
import aiohttp
from app.config import get_secret


class NaverBookScraper:
    NAVER_API_BOOK = "https://openapi.naver.com/v1/search/book"
    NAVER_API_ID = get_secret("NAVER_API_ID")
    NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["items"]

    def unit_url(self, keyword, start):
        return {
            "url": f"{self.NAVER_API_BOOK}?query={keyword}&display=20&start={start}",
            "headers": {
                "X-Naver-Client-Id": self.NAVER_API_ID,
                "X-Naver-Client-Secret": self.NAVER_API_SECRET
            }
        }

    async def search(self, keyword, total_page):
        apis = [self.unit_url(keyword, 1 + i*20) for i in range(total_page)]
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            all_data = await asyncio.gather(
                *[NaverBookScraper.fetch(session, api["url"], api["headers"]) for api in apis]
            )
            result = []
            for data in all_data:
                if data is not None:
                    for book in data:
                        result.append(book)
            return result

    def run(self, keyword, total_page):
        return asyncio.run(self.search(keyword, total_page))


if __name__ == "__main__":
    scraper = NaverBookScraper()
    print(len(scraper.run("파이썬", 1)))
# import aiohttp
# import asyncio
# from app.config import get_secret


# class NaverBookScraper:

#     def __init__(self):
#         self.keyword: str = ""
#         self.price: list = []
#         self.image: list = []
#         self.base_url: str = "https://openapi.naver.com/v1/search/image"

#     def get_keyword(self, keyword):
#         self.keyword = keyword

#     async def image_fetcher(self, session, url):
#         headers = {
#             "X-Naver-Client-Id": get_secret("X-Naver-Client-Id"),
#             "X-Naver-Client-Secret": get_secret("X-Naver-Client-Secret")
#         }

#         async with session.get(url, headers=headers) as response:
#             result = await response.json()
#             items = result["items"]
#             images = [item["link"]for item in items]
#             self.image = images

#     async def image_save(self):
#         urls = [
#             f"{self.base_url}?query={self.keyword}&display20&start={1+ i*20}" for i in range(1, 10)]
#         async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
#             await asyncio.gather(*[self.image_fetcher(session, url) for url in urls])

#     def search(self, keyword):
#         self.get_keyword(keyword)
#         self.image_save()
#         return {"keyword": self.keyword, "img": self.image}


# scraper = NaverBookScraper()
