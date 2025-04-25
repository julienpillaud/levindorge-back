from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.API_VERSION,
        swagger_ui_parameters={
            "tryItOutEnabled": True,
            "displayRequestDuration": True,
        },
    )

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.get("/")
    async def root():  # type: ignore[reportUnusedFunction]
        return {
            "title": settings.PROJECT_NAME,
            "version": settings.API_VERSION,
        }

    return app
