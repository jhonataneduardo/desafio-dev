from pydantic import BaseModel

from domain.entities import EntityTransaction


class InputTransactionDTO(BaseModel):
    type: int
    date: str
    card_number: str
    national_id: str
    hour: str
    store_name: str
    store_owner: str
    amount: float

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "date": self.date,
            "card_number": self.card_number,
            "national_id": self.national_id,
            "hour": self.hour,
            "store_name": self.store_name,
            "store_owner": self.store_owner,
            "amount": self.amount
        }