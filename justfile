default:
    just --list

# Run the application
init:
    uv sync --all-extras
    uv run pre-commit install

run-app port="8000":
    uv run uvicorn app.core.app:app \
    --port {{port}} \
    --reload --reload-dir app \
    --log-config app/core/logging/config.json

# Development tools
pre-commit:
	uv run pre-commit run --all-files

lint:
	uv run ruff format
	uv run ruff check --fix || true
	uv run mypy .

tests *options="--log-cli-level=INFO":
    uv run pytest {{options}}

coverage source="app":
	uv run coverage run --source={{source}} -m pytest
	uv run coverage report --show-missing
	uv run coverage html
