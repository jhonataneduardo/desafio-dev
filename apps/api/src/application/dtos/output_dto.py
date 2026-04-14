from datetime import datetime, date, time
from pydantic import BaseModel, ConfigDict


class OutputTransactionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: int
    date: date
    card_number: str
    national_id: str
    hour: time
    store_name: str
    store_owner: str
    amount: float
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def model_validate_from_entity(cls, entity: "EntityTransaction") -> "OutputTransactionDTO":
        return cls.model_validate(entity)
