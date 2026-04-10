from abc import ABC, abstractmethod

from domain.entities import EntityTransaction


class TransactionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, transaction: EntityTransaction):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, transaction_id: int) -> EntityTransaction:
        raise NotImplementedError
