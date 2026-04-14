from domain.entities import TransactionQuery
from domain.repositories import TransactionRepositoryInterface


class SearchTransactionsUseCase:
    def __init__(self, transaction_repository: TransactionRepositoryInterface):
        self.transaction_repository = transaction_repository

    def execute(self, params: TransactionQuery):
        return self.transaction_repository.find_all(params)
