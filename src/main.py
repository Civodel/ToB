from fastapi import FastAPI

from src.routes.conversation import router

app = FastAPI(
    title="TwentyOneBot:Pilot01",
    description="Una API para  generar discuciones sobre cualquier tema",
    version="1.0.0"
)


@app.get("/", summary="Saludo de bienvenida")
def read_root():
    return {"message": "Hola, soy TwentyOneBot:Pilot01, pero puedes decirme tob"}


app.include_router(router)
