from typing import List
from abc import ABC, abstractmethod

from domain.entities import EntityTransaction, TransactionQuery


class TransactionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, transaction: EntityTransaction) -> EntityTransaction:
        raise NotImplementedError

    @abstractmethod
    def save_batch(self, transactions: List[EntityTransaction]) -> List[EntityTransaction]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self, params: TransactionQuery) -> List[EntityTransaction]:
        raise NotImplementedError
