from abc import ABC, abstractmethod


class TransactionRepository(ABC):
    @abstractmethod
    def save(self, transaction):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, transaction_id):
        raise NotImplementedError
