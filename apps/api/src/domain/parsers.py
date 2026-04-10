from typing import List

from abc import ABC, abstractmethod
from domain.entities import EntityTransaction


class CnabParserInterface(ABC):
    @abstractmethod
    def parse(self, content: bytes) -> List[EntityTransaction]:
        raise NotImplementedError
