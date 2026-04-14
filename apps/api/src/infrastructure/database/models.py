from datetime import date, time, datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, DateTime, SmallInteger, Date, Time
from sqlalchemy.orm import Mapped, mapped_column

from .session import Base


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True)
    type: Mapped[int] = mapped_column(SmallInteger)
    date: Mapped[date] = mapped_column(Date, index=True)
    card_number: Mapped[str] = mapped_column(String(255))
    national_id: Mapped[str] = mapped_column(String(255))
    hour: Mapped[time] = mapped_column(Time)
    store_name: Mapped[str] = mapped_column(String(255), index=True)
    store_owner: Mapped[str] = mapped_column(String(255))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True)
