from infrastructure.database import session

from application.use_cases import ImportTrasactionsUseCase
from infrastructure.repositories import TransactionRepository


class ImportTransactionsUseCaseFactory:
    def __init__(self):
        self.transaction_repository = TransactionRepository()

    def create(self) -> ImportTrasactionsUseCase:
        return ImportTrasactionsUseCase(self.transaction_repository)


def get_import_transactions_use_case():
    factory = ImportTransactionsUseCaseFactory()
    return factory.create()
