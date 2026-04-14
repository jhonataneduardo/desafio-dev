from enum import Enum
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from domain.entities import TransactionQuery
from application.usecases.search_transactions_use_case import SearchTransactionsUseCase
from infrastructure.dependencies import get_search_transactions_use_case
from presentation.responses.envelope import ResponseEnvelope

TransactionRouter = APIRouter(prefix="/transactions", tags=["transactions"])


class GroupByEnum(str, Enum):
    store = "store"


@TransactionRouter.get("/")
async def get_transactions(
    group_by: GroupByEnum | None = None,
    page: int = 1,
    page_size: int = 50,
    use_case: SearchTransactionsUseCase = Depends(
        get_search_transactions_use_case)
):
    params = TransactionQuery(group_by=group_by, page=page, page_size=page_size)
    result = use_case.execute(params)
    response_data = ResponseEnvelope(
        success=True,
        data=result,
        message="Transactions retrieved successfully",
    )
    return JSONResponse(
        status_code=200,
        content=response_data.model_dump(mode="json")
    )
