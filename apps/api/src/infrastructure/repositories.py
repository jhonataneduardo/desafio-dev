from domain.entities import EntityTransaction
from domain.repositories import TransactionRepositoryInterface

from infrastructure.database import TransactionModel


class TransactionRepository(TransactionRepositoryInterface):
    def save(self, transaction: EntityTransaction) -> EntityTransaction:
        transaction = TransactionModel.create(
            type=transaction.type.value,
            date=transaction.date,
            card_number=transaction.card_number,
            national_id=transaction.national_id,
            hour=transaction.hour,
            store_id=transaction.store_id,
            amount=transaction.amount,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at
        )
        return transaction
