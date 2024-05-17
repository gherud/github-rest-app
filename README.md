# ada-task
ADA project recruitment task

## Run application

Redis:
```sh
docker run -d -p 6379:6379 redis
```

NOTE: Prerequisite to run app is to export `GITHUB_ACCESS_TOKEN`.
```sh
export GITHUB_ACCESS_TOKEN="<VALUE_HERE>"
```

Run app:
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
poetry run ada
```

## Testing

pre-commit:
```sh
poetry run pre-commit run --all-files
```

Unit tests:
```sh
poetry run pytest
# or, with coverage:
poetry run pytest --cov src/ada
```

## Improvements

- Add Dev Container support [DevContainers](https://www.google.com/search?client=safari&rls=en&q=dev+containers&ie=UTF-8&oe=UTF-8) for consistent development environment,
- Add integration tests (e.g. using `pytest-bdd` library),
- Add GitHub actions workflows for linting, unit tests and deployment,
