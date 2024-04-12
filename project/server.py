import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

import project.fetch_comic_explanation_service
import project.fetch_random_comic_service
import project.fetch_user_preferences_service
import project.record_interaction_service
import project.update_user_preferences_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="correcthorsebatterystaple",
    lifespan=lifespan,
    description="To create a tool that returns a random xkcd comic each time it is called, the following steps and considerations were gathered based on user requirements and technical research:\n\n1. **Feature Requirements**:\n   - The tool should offer additional features beyond simply fetching the comic, such as providing explanations or context for each comic.\n   - Users prefer the comic to be random but from a specific range, specifically from the latest 100 comics, to ensure relevance to current events or themes.\n   - Implement caching for previously fetched xkcd comics to reduce API calls and load times, enhancing user experience.\n\n2. **Technical Stack**:\n   - Programming language: Python, for its ease of handling API requests and data manipulation.\n   - API Framework: FastAPI, for creating an asynchronous API that can handle external API requests efficiently.\n   - Database: PostgreSQL, for storing information about the cached comics.\n   - ORM: Prisma, to interface with the database smoothly and manage data models easily.\n\n3. **Implementation Details**:\n   - Utilize the 'random' Python module to select a comic number randomly within the latest 100 comics.\n   - Use the public xkcd API to fetch comics based on the generated random number. The API provides necessary details like the comic's title, URL, image link, and alt text without requiring an API key.\n   - Integrate the `httpx` library within the FastAPI application to handle asynchronous HTTP requests to the xkcd API.\n   - Develop a caching mechanism using PostgreSQL and Prisma to store comic details and serve them on subsequent requests without hitting the xkcd API to reduce load times and API calls.\n\nThis project aims to provide users with a seamless experience in discovering xkcd comics, with an emphasis on relevance, speed, and additional contextual insights.",
)


@app.get(
    "/explanation/{comicId}",
    response_model=project.fetch_comic_explanation_service.FetchComicExplanationResponse,
)
async def api_get_fetch_comic_explanation(
    comicId: str,
) -> project.fetch_comic_explanation_service.FetchComicExplanationResponse | Response:
    """
    Retrieves explanations for a given comic.
    """
    try:
        res = await project.fetch_comic_explanation_service.fetch_comic_explanation(
            comicId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/preferences/update",
    response_model=project.update_user_preferences_service.UpdateUserPreferencesResponse,
)
async def api_put_update_user_preferences(
    user_id: str,
    view_range_min: Optional[int],
    view_range_max: Optional[int],
    preferred_categories: List[str],
) -> project.update_user_preferences_service.UpdateUserPreferencesResponse | Response:
    """
    Updates user-specific settings and viewing preferences.
    """
    try:
        res = await project.update_user_preferences_service.update_user_preferences(
            user_id, view_range_min, view_range_max, preferred_categories
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/preferences",
    response_model=project.fetch_user_preferences_service.UserPreferencesResponse,
)
async def api_get_fetch_user_preferences() -> project.fetch_user_preferences_service.UserPreferencesResponse | Response:
    """
    Fetches the current settings and preferences for the user.
    """
    try:
        res = await project.fetch_user_preferences_service.fetch_user_preferences()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/analytics/interaction",
    response_model=project.record_interaction_service.RecordInteractionResponse,
)
async def api_post_record_interaction(
    eventType: str, data: Dict[str, Any], userId: Optional[str]
) -> project.record_interaction_service.RecordInteractionResponse | Response:
    """
    Logs user interactions for analytics purposes.
    """
    try:
        res = await project.record_interaction_service.record_interaction(
            eventType, data, userId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/comic/random",
    response_model=project.fetch_random_comic_service.FetchRandomComicResponse,
)
async def api_get_fetch_random_comic() -> project.fetch_random_comic_service.FetchRandomComicResponse | Response:
    """
    Fetches a random xkcd comic based on user preferences and caches it.
    """
    try:
        res = await project.fetch_random_comic_service.fetch_random_comic()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
