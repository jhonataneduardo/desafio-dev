from application.dtos import InputTransactionDTO
from domain.repositories import TransactionRepository


class ImportTrasactionsUseCase:
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, input_transactions: list[InputTransactionDTO]):
        for transaction in input_transactions:
            self.transaction_repository.save(transaction)