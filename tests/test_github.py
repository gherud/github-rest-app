import pytest
from ada import github


class TestGetHeaders:

    test_cases = [
        (
            "test-github-token",
            {
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer test-github-token",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        ),
        (
            "another-test-github-token",
            {
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer another-test-github-token",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        ),
    ]

    @pytest.mark.parametrize("token, expected", test_cases)
    def test_get_headers(self, token, expected):
        assert expected == github.get_headers(token)


class TestGetRepo:

    @pytest.mark.asyncio
    async def test_get_repo(self, mocker):
        # Mocks
        mock_client = mocker.AsyncMock()
        mock_client.__aenter__.return_value.get.return_value = mocker.Mock(
            json=lambda: {"json": "response"}
        )
        mocker.patch("ada.github.httpx.AsyncClient", return_value=mock_client)
        mocker.patch("ada.github.get_headers")

        # Execution
        response = github.get_repo(org="test-org", repo_name="test-repo", token="test-token")
        assert {"json": "response"} == await response

        # Assertions
        mock_client.assert_has_calls(
            [
                mocker.call.__aenter__(),
                mocker.call.__aenter__().get(
                    "https://api.github.com/repos/test-org/test-repo",
                    headers=github.get_headers.return_value,
                ),
            ]
        )
        github.get_headers.assert_called_once_with("test-token")
