import os
from collections.abc import Iterator

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from pymongo import MongoClient
from pymongo.database import Database

from app.api.app import create_app
from app.api.dependencies import get_settings
from app.core.config import Settings
from app.infrastructure.repository.base import MongoDocument

pytest_plugins = [
    "tests.fixtures.factories.fixtures",
    "tests.fixtures.repositories",
]

load_dotenv()


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(
        MONGO_USER=os.environ["MONGO_USER"],
        MONGO_PASSWORD=os.environ["MONGO_PASSWORD"],
        MONGO_HOST=os.environ["MONGO_HOST"],
        MONGO_DATABASE=os.environ["MONGO_DATABASE"],
    )


@pytest.fixture
def database(settings: Settings) -> Iterator[Database[MongoDocument]]:
    client: MongoClient[MongoDocument] = MongoClient(settings.MONGO_URI)
    database: Database[MongoDocument] = client[settings.MONGO_DATABASE]
    yield database
    for collection in database.list_collection_names():
        database[collection].delete_many({})
    client.close()


@pytest.fixture(scope="session")
def client(settings: Settings) -> Iterator[TestClient]:
    def get_settings_override() -> Settings:
        return settings

    app = create_app(settings=settings)

    app.dependency_overrides[get_settings] = get_settings_override
    yield TestClient(app)
    app.dependency_overrides.clear()
