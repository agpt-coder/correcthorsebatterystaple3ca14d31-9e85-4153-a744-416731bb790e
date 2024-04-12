from datetime import datetime
from typing import Any, Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class RecordInteractionResponse(BaseModel):
    """
    Describes the outcome of an attempt to record a user interaction, primarily confirming receipt of the data.
    """

    success: bool
    message: str


async def record_interaction(
    eventType: str, data: Dict[str, Any], userId: Optional[str]
) -> RecordInteractionResponse:
    """
    Logs user interactions for analytics purposes.

    Args:
        eventType (str): Specifies the type of interaction being recorded, such as 'comic_view', 'favorite_added', etc.
        data (Dict[str, Any]): A JSON-serializable dictionary containing metadata about the event, such as which comic was viewed, timestamp of interaction, etc.
        userId (Optional[str]): The identifier of the user who triggered the event, to enable user-specific analytics.

    Returns:
        RecordInteractionResponse: Describes the outcome of an attempt to record a user interaction, primarily confirming receipt of the data.
    """
    try:
        await prisma.models.Analytics.prisma().create(
            data={"eventType": eventType, "data": data, "occurredAt": datetime.now()}
        )
        return RecordInteractionResponse(
            success=True, message="Interaction recorded successfully."
        )
    except Exception as e:
        return RecordInteractionResponse(
            success=False, message=f"Failed to record interaction: {str(e)}"
        )
