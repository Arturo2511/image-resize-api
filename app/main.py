from fastapi import FastAPI
from app.api import router

app = FastAPI()

app.include_router(router)


@app.get("/ping")
async def ping():
    return {"message": "Pong!"}