from typing import List
from sqlalchemy import insert
from sqlalchemy.orm import Session

from domain.entities import TypeTransaction, EntityTransaction, TransactionQuery
from domain.repositories import TransactionRepositoryInterface

from infrastructure.database.models import TransactionModel


class TransactionRepository(TransactionRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def save(self, transaction: EntityTransaction) -> EntityTransaction:
        txn_model = self._to_model(transaction)
        self.db.add(txn_model)
        self.db.commit()
        self.db.refresh(txn_model)
        return self._to_entity(txn_model)

    def save_batch(self, transactions: List[EntityTransaction]) -> List[EntityTransaction]:
        if not transactions:
            return []

        values = [
            {
                "type": t.type.value if isinstance(t.type, TypeTransaction) else t.type,
                "date": t.date,
                "card_number": t.card_number,
                "national_id": t.national_id,
                "hour": t.hour,
                "store_name": t.store_name,
                "store_owner": t.store_owner,
                "amount": t.amount,
                "created_at": t.created_at,
                "updated_at": t.updated_at,
            }
            for t in transactions
        ]

        stmt = insert(TransactionModel).values(values).returning(TransactionModel)
        result = self.db.scalars(stmt).all()
        self.db.commit()

        return [self._to_entity(r) for r in result]

    def find_all(self, params: TransactionQuery) -> List[EntityTransaction]:
        query = self.db.query(TransactionModel)

        if params.group_by == "store":
            query = query.order_by(TransactionModel.store_name)

        query = query.offset((params.page - 1) * params.page_size).limit(params.page_size)

        transactions = query.all()
        return [self._to_entity(t) for t in transactions]

    def _to_model(self, entity: EntityTransaction) -> TransactionModel:
        return TransactionModel(
            type=entity.type.value if isinstance(
                entity.type, TypeTransaction) else entity.type,
            date=entity.date, card_number=entity.card_number,
            national_id=entity.national_id, hour=entity.hour,
            store_name=entity.store_name, store_owner=entity.store_owner,
            amount=entity.amount, created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def _to_entity(self, model: TransactionModel) -> EntityTransaction:
        return EntityTransaction(
            id=model.id, type=TypeTransaction.from_value(model.type),
            date=model.date, card_number=model.card_number,
            national_id=model.national_id, hour=model.hour,
            store_name=model.store_name, store_owner=model.store_owner,
            amount=float(model.amount), created_at=model.created_at,
            updated_at=model.updated_at,
        )
