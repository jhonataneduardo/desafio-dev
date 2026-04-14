from typing import List, Dict
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, UploadFile, File

from domain.entities import TransactionQuery
from application.usecases.search_transactions_use_case import SearchTransactionsUseCase
from application.usecases.get_transactions_summary_use_case import GetTransactionsSummaryUseCase
from application.usecases.process_cnab_use_case import ProcessCnabFileUseCase
from application.dtos.output_dto import OutputTransactionDTO
from infrastructure.dependencies import get_search_transactions_use_case, get_process_cnab_file_use_case, get_transactions_summary_use_case
from presentation.responses.envelope import ResponseEnvelope

TransactionRouter = APIRouter(prefix="/transactions", tags=["transactions"])


@TransactionRouter.post("/import", response_model=ResponseEnvelope[List[OutputTransactionDTO]])
async def import_cnab(
    file: UploadFile = File(),
    use_case: ProcessCnabFileUseCase = Depends(get_process_cnab_file_use_case),
):
    content = await file.read()
    transactions = use_case.execute(content)
    response_data = ResponseEnvelope(
        success=True,
        data=[
            OutputTransactionDTO.model_validate_from_entity(t)
            for t in transactions
        ],
        message="Arquivo CNAB processado com sucesso"
    )
    return JSONResponse(
        status_code=201,
        content=response_data.model_dump(mode="json")
    )


@TransactionRouter.get("/", response_model=ResponseEnvelope[List[OutputTransactionDTO]])
async def get_transactions(
    page: int = 1,
    page_size: int = 50,
    use_case: SearchTransactionsUseCase = Depends(get_search_transactions_use_case)
):
    params = TransactionQuery(group_by=None, page=page, page_size=page_size)
    transactions = use_case.execute(params)
    response_data = ResponseEnvelope(
        success=True,
        data=[
            OutputTransactionDTO.model_validate_from_entity(t)
            for t in transactions
        ],
        message="Transactions retrieved successfully",
    )
    return JSONResponse(
        status_code=200,
        content=response_data.model_dump(mode="json")
    )


@TransactionRouter.get("/summary", response_model=ResponseEnvelope[Dict[str, List[OutputTransactionDTO]]])
async def get_transactions_summary(
    page: int = 1,
    page_size: int = 50,
    use_case: GetTransactionsSummaryUseCase = Depends(get_transactions_summary_use_case)
):
    params = TransactionQuery(group_by="store", page=page, page_size=page_size)
    grouped = use_case.execute(params)
    
    data = {
        store: [OutputTransactionDTO.model_validate_from_entity(t) for t in trans]
        for store, trans in grouped.items()
    }
    
    response_data = ResponseEnvelope(
        success=True,
        data=data,
        message="Store summary retrieved successfully",
    )
    return JSONResponse(
        status_code=200,
        content=response_data.model_dump(mode="json")
    )
