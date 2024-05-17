import json
import logging
import os
from http import HTTPStatus

import aioredis
from ada import github
from ada.models.output import GetRepoInsightsOutputModel
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)
redis = aioredis.from_url("redis://localhost")

app = FastAPI()


@app.middleware("http")
async def cache(request: Request, call_next):
    """Cache the response of GET requests."""
    cache_key = request.url.path
    if request.method == "GET":
        cached_data = await redis.get(cache_key)
        if cached_data:
            logger.debug("Returning cached data")
            return JSONResponse(content=json.loads(cached_data))
    response = await call_next(request)
    if request.method == "GET":
        await redis.set(cache_key, response)
    return response


@app.get(
    "/repositories/{owner}/{repository_name}",
    response_model=GetRepoInsightsOutputModel,
    status_code=HTTPStatus.OK,
)
async def get_repo_insights(owner: str, repository_name: str):
    """Get insights about a GitHub repository."""
    logger.debug("Fetching data from GitHub.")
    repo_details = await github.get_repo(
        org=owner, repo_name=repository_name, token=GITHUB_ACCESS_TOKEN
    )
    return GetRepoInsightsOutputModel(
        cloneUrl=repo_details["clone_url"],
        createdAt=repo_details["created_at"],
        description=repo_details["description"],
        fullName=repo_details["full_name"],
        stars=repo_details["stargazers_count"],
    )


def main():
    """Run the FastAPI application."""
    import uvicorn

    logger.setLevel(logging.DEBUG)

    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    main()
