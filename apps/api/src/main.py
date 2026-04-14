from fastapi.responses import JSONResponse
from presentation.routers.transactions_routers import TransactionRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request

from presentation.responses.envelope import ResponseEnvelope
from domain.exceptions import CnabException

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://web:3000"],
)


@app.exception_handler(CnabException)
async def domain_exception_handler(request: Request, exc: CnabException):
    return JSONResponse(status_code=400, content=ResponseEnvelope(
        success=False, data=None, error=exc.message,
        message="Business rule validation failed"
    ).model_dump(mode="json"))


@app.exception_handler(Exception)
async def generic_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=ResponseEnvelope(
        success=False, data=None, error=str(exc),
        message="Internal server error"
    ).model_dump(mode="json"))


@app.get("/health")
async def health():
    return {"message": "ok"}

app.include_router(TransactionRouter, prefix="/api/v1")
