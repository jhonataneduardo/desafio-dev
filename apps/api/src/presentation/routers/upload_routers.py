from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, UploadFile, File

from domain.exceptions import InvalidFileException
from application.dtos.output_dto import OutputTransactionDTO
from application.usecases.process_cnab_use_case import ProcessCnabFileUseCase
from infrastructure.dependencies import get_process_cnab_file_use_case
from presentation.responses.envelope import ResponseEnvelope

UploadRouter = APIRouter(prefix="/uploads", tags=["uploads"])


@UploadRouter.post("/cnab", response_model=ResponseEnvelope[List[OutputTransactionDTO]])
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
    )
    return JSONResponse(
        status_code=201,
        content=response_data.model_dump(mode="json")
    )
