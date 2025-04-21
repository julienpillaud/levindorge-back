from fastapi import FastAPI

app = FastAPI(
    title="Le Vin d'Orge",
    version="0.0.1",
    swagger_ui_parameters={
        "tryItOutEnabled": True,
        "displayRequestDuration": True,
    },
)


@app.get("/")
async def root():
    return {
        "title": "Le Vin d'Orge",
        "version": "0.0.1",
    }
