FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

COPY .python-version /code/.python-version
COPY pyproject.toml /code/pyproject.toml
COPY uv.lock /code/uv.lock

RUN uv sync

COPY app/ /code/app

CMD ["uv", "run", "uvicorn", "app.core.app:app", "--host", "0.0.0.0"]
