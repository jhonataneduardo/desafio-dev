from typing import List

from domain.entities import EntityTransaction
from domain.parsers import CnabParserInterface
from domain.repositories import TransactionRepositoryInterface

MAX_FILE_SIZE = 10 * 1024 * 1024


class ProcessCnabFileUseCase:
    def __init__(self, cnab_parser: CnabParserInterface, transaction_repository: TransactionRepositoryInterface):
        self.cnab_parser = cnab_parser
        self.transaction_repository = transaction_repository

    def execute(self, content: bytes) -> List[EntityTransaction]:
        transactions = self.cnab_parser.parse(content)
        return self.transaction_repository.save_batch(transactions)
