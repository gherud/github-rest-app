import pytest
from ada.models import output


class TestGetRepoInsights:

    @pytest.fixture
    def expected(self):
        return output.GetRepoInsightsOutputModel(
            cloneUrl="https://github.com/test-org/test-repo.git",
            createdAt="2022-01-01T00:00:00Z",
            description="Test description",
            fullName="test-org/test-repo",
            stars=10,
        )

    @pytest.mark.asyncio
    async def test_get_repo_insights(self, mocker, expected):
        from ada import main

        # Mocks
        mocker.patch("ada.main.GITHUB_ACCESS_TOKEN", "test-github-token")
        mocker.patch(
            "ada.github.get_repo",
            return_value={
                "clone_url": "https://github.com/test-org/test-repo.git",
                "created_at": "2022-01-01T00:00:00Z",
                "description": "Test description",
                "full_name": "test-org/test-repo",
                "stargazers_count": 10,
            },
        )

        # Execution
        assert expected == await main.get_repo_insights("test-org", "test-repo")

        # Assertions
        main.github.get_repo.assert_called_once_with(
            org="test-org", repo_name="test-repo", token="test-github-token"
        )
