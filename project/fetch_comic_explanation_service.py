import prisma
import prisma.models
from pydantic import BaseModel


class FetchComicExplanationResponse(BaseModel):
    """
    Encapsulates the explanation for a given comic, including any relevant context or additional details.
    """

    comicId: str
    title: str
    explanation: str
    source: str
    updatedAt: str


async def fetch_comic_explanation(comicId: str) -> FetchComicExplanationResponse:
    """
    Retrieves explanations for a given comic.

    Args:
    comicId (str): The ID of the comic for which the explanation is being requested.

    Returns:
    FetchComicExplanationResponse: Encapsulates the explanation for a given comic, including any relevant context or additional details.
    """
    explanation = await prisma.models.Explanation.prisma().find_unique(
        where={"comicId": comicId}
    )
    if not explanation:
        raise ValueError(f"No explanation found for comicId: {comicId}")
    comic = await prisma.models.Comic.prisma().find_unique(
        where={"id": explanation.comicId}
    )
    if not comic:
        raise ValueError(f"No comic found with ID: {comicId}")
    return FetchComicExplanationResponse(
        comicId=comic.id,
        title=comic.title,
        explanation=explanation.content,
        source="User Generated Content",
        updatedAt=explanation.updatedAt.strftime("%Y-%m-%d %H:%M:%S"),
    )


async def main():
    comic_id = "some-comic-id"
    try:
        explanation_response = await fetch_comic_explanation(comic_id)
        print(explanation_response)
    except ValueError as e:
        print(f"Error: {e}")
