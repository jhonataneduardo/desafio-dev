from fastapi import Depends
from sqlalchemy.orm import Session

from infrastructure.parsers import Cnab80Parser
from application.usecases.process_cnab_use_case import ProcessCnabFileUseCase
from infrastructure.repositories.transaction_repository import TransactionRepository
from application.usecases.search_transactions_use_case import SearchTransactionsUseCase
from application.usecases.get_transactions_summary_use_case import GetTransactionsSummaryUseCase

from infrastructure.database.session import get_db


def get_process_cnab_file_use_case(db: Session = Depends(get_db)):
    parser = Cnab80Parser()
    repository = TransactionRepository(db=db)
    return ProcessCnabFileUseCase(parser, repository)


def get_search_transactions_use_case(db: Session = Depends(get_db)):
    repository = TransactionRepository(db=db)
    return SearchTransactionsUseCase(repository)

def get_transactions_summary_use_case(db: Session = Depends(get_db)):
    repository = TransactionRepository(db=db)
    return GetTransactionsSummaryUseCase(repository)
