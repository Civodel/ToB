#main from eva01
#you can (NOT) chat Alone
from fastapi import FastAPI
from src.routes.conversation import router


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hola, Chavots test"}

app.include_router(router)
