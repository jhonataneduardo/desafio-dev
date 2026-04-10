from infrastructure.parsers import CnabParser
from infrastructure.database import session

from application.use_cases import ImportCnabTransactionsUseCase
from infrastructure.repositories import TransactionRepository


class ImportCnabTransactionsUseCaseFactory:
    def __init__(self):
        self.parser = CnabParser()
        self.transaction_repository = TransactionRepository()

    def create(self) -> ImportCnabTransactionsUseCase:
        return ImportCnabTransactionsUseCase(self.parser, self.transaction_repository)


def get_import_cnab_transactions_use_case():
    factory = ImportCnabTransactionsUseCaseFactory()
    return factory.create()
