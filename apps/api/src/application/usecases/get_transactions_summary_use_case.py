from domain.entities import TransactionQuery
from domain.repositories import TransactionRepositoryInterface


class GetTransactionsSummaryUseCase:
    def __init__(self, transaction_repository: TransactionRepositoryInterface):
        self.transaction_repository = transaction_repository

    def execute(self, params: TransactionQuery):
        transactions = self.transaction_repository.find_all(params)
        
        grouped = {}
        for t in transactions:
            if t.store_name not in grouped:
                grouped[t.store_name] = []
            grouped[t.store_name].append(t)
        return grouped
