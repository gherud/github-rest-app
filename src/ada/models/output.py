from pydantic import BaseModel


class GetRepoInsightsOutputModel(BaseModel):
    """GET /repositories/{owner}/{repository_name} response model."""

    cloneUrl: str
    createdAt: str
    description: str | None
    fullName: str
    stars: int
