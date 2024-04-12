import random
from datetime import datetime

import httpx
from pydantic import BaseModel


class FetchRandomComicResponse(BaseModel):
    """
    Response object containing details about the fetched random XKCD comic.
    """

    id: str
    num: int
    title: str
    img: str
    alt: str
    dateFetched: str


async def fetch_random_comic() -> FetchRandomComicResponse:
    """
    Fetches a random xkcd comic based on user preferences and caches it.

    Returns:
    FetchRandomComicResponse: Response object containing details about the fetched random XKCD comic.
    """
    LATEST_XKCD_URL = "https://xkcd.com/info.0.json"
    XKCD_BASE_URL = "https://xkcd.com/{}/info.0.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(LATEST_XKCD_URL)
        latest_comic = response.json()
        latest_comic_num = int(latest_comic["num"])
        random_comic_num = random.randint(
            max(1, latest_comic_num - 99), latest_comic_num
        )
        random_comic_url = XKCD_BASE_URL.format(random_comic_num)
        response = await client.get(random_comic_url)
        comic = response.json()
        return FetchRandomComicResponse(
            id=str(comic["num"]),
            num=comic["num"],
            title=comic["title"],
            img=comic["img"],
            alt=comic["alt"],
            dateFetched=datetime.now().isoformat(),
        )
