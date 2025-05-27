from fastapi import FastAPI

from src.database.db import engine
from src.database.models import Base
from src.routes.conversation import router
from src.slack.slack_integration import slack_router

app = FastAPI(
    title="TwentyOneBot:Pilot01",
    description="Una API para  generar discuciones sobre cualquier tema",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


@app.get("/", summary="Saludo de bienvenida")
def read_root():
    return {"message": "Hola, soy TwentyOneBot:Pilot01, pero puedes decirme tob"}


app.include_router(router)
app.include_router(slack_router)
