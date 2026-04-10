from fastapi import APIRouter, Depends

from application.use_cases import ImportTrasactionsUseCase
from infrastructure.factories import get_import_transactions_use_case

ImportRouter = APIRouter(prefix="/imports", tags=["imports"])


@ImportRouter.get("/cnab")
async def import_cnab(use_case: ImportTrasactionsUseCase = Depends(get_import_transactions_use_case)):
    return {"message": "ok"}
