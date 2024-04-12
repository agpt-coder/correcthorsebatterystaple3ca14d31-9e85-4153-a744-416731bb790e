from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserPreferencesRequest(BaseModel):
    """
    This model captures the essential information required to update a user's comic viewing preferences. It includes the user's ID for lookup and preference details for updates.
    """

    user_id: str
    view_range_min: Optional[int] = None
    view_range_max: Optional[int] = None
    preferred_categories: List[str]


class UpdateUserPreferencesResponse(BaseModel):
    """
    The response model confirms that the user's preferences were updated successfully and returns the updated preferences.
    """

    success: bool
    updated_preferences: UpdateUserPreferencesRequest


async def update_user_preferences(
    user_id: str,
    view_range_min: Optional[int],
    view_range_max: Optional[int],
    preferred_categories: List[str],
) -> UpdateUserPreferencesResponse:
    """
    Updates user-specific settings and viewing preferences.

    Args:
    user_id (str): The unique identifier of the user whose preferences are being updated.
    view_range_min (Optional[int]): The minimum comic number considered for random selection, allowing users to specify a range.
    view_range_max (Optional[int]): The maximum comic number considered for random selection, allowing users to specify a range.
    preferred_categories (List[str]): A list of preferred categories or themes within the xkcd comics that the user wants to see more often.

    Returns:
    UpdateUserPreferencesResponse: The response model confirms that the user's preferences were updated successfully and returns the updated preferences.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if not user:
        return UpdateUserPreferencesResponse(success=False, updated_preferences=None)
    new_preferences = {
        "view_range_min": view_range_min,
        "view_range_max": view_range_max,
        "preferred_categories": preferred_categories,
    }
    updated_user = await prisma.models.User.prisma().update(
        where={"id": user_id}, data={"preferences": new_preferences}
    )
    updated_request = UpdateUserPreferencesRequest(
        user_id=user_id,
        view_range_min=view_range_min,
        view_range_max=view_range_max,
        preferred_categories=preferred_categories,
    )
    return UpdateUserPreferencesResponse(
        success=True, updated_preferences=updated_request
    )
