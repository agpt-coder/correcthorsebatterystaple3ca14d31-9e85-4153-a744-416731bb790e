from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class UserPreferencesResponse(BaseModel):
    """
    Provides the current settings and preferences for the user, including their favorite comics and any viewing preferences, such as display mode or range selection for random comic fetching.
    """

    favorites: List[int]
    recent_views: List[int]
    display_mode: str
    random_range: int


async def fetch_user_preferences() -> UserPreferencesResponse:
    """
    Fetches the current settings and preferences for the user from the database.

    Queries the database to obtain the user's favorite comics and recent views, as well as their viewing preferences
    like display mode and the range used for fetching random comics. Assumes there's an authenticated user context available.

    Returns:
        UserPreferencesResponse: Provides the current settings and preferences for the user, including their favorite comics and any viewing preferences, such as display mode or range selection for random comic fetching.
    """
    current_user_id = "example_current_user_id"
    user_info = await prisma.models.User.prisma().find_unique(
        where={"id": current_user_id}, include={"Favorites": True, "ViewHistory": True}
    )
    if user_info is None:
        raise ValueError("prisma.models.User not found")
    favorites = [favorite.comicId for favorite in user_info.Favorites]
    recent_views = [view.comicId for view in user_info.ViewHistory]
    display_mode = "dark"
    random_range = 100
    return UserPreferencesResponse(
        favorites=favorites,
        recent_views=recent_views,
        display_mode=display_mode,
        random_range=random_range,
    )
