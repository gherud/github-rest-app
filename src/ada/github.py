import logging

import httpx

BASE_GITHUB_API_URL = "https://api.github.com"
logger = logging.getLogger(__file__)


def get_headers(token: str) -> dict:
    """Get the headers for the GitHub API requests."""
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


async def get_repo(*, org: str, repo_name: str, token: str):
    url = f"{BASE_GITHUB_API_URL}/repos/{org}/{repo_name}"
    async with httpx.AsyncClient() as client:
        headers = get_headers(token)
        response = await client.get(url, headers=headers)
        return response.json()
