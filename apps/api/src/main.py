from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from presentation.routers import ImportRouter

app = FastAPI()


@app.get("/health")
async def health():
    return {"message": "ok"}

app.include_router(ImportRouter, prefix="/api/v1")
