from enum import Enum
from typing import Dict
from datetime import date, time, datetime
from dataclasses import field, dataclass, asdict


class TypeTransaction(Enum):
    DEBITO = 1
    BOLETO = 2
    FINANCIAMENTO = 3
    CREDITO = 4
    RECEBIMENTO_EMPRESTIMO = 5
    VENDAS = 6
    TED = 7
    DOC = 8
    ALUGUEL = 9

    @classmethod
    def from_value(cls, value):
        return cls(value=value)


@dataclass
class EntityBase:
    id: int = field(default=None, repr=False, kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    updated_at: datetime = field(default=None, kw_only=True)


@dataclass
class EntityTransaction(EntityBase):
    type: TypeTransaction
    date: date
    card_number: str
    national_id: str
    hour: time
    store_name: str
    store_owner: str
    amount: float

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict):
        data_copy = data.copy()
        return cls(**data_copy)


@dataclass
class TransactionQuery:
    group_by: str | None = None
    page: int = 1
    page_size: int = 50
