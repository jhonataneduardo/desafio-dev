import os

from playhouse.shortcuts import model_to_dict
from peewee import PostgresqlDatabase, Model, CharField, DecimalField, DateTimeField, SmallIntegerField, DateField, TimeField


session = PostgresqlDatabase(
    database=os.environ.get("DATABASE_NAME"),
    host=os.environ.get("DATABASE_HOST"),
    port=os.environ.get("DATABASE_PORT"),
    user=os.environ.get("DATABASE_USER"),
    password=os.environ.get("DATABASE_PASSWORD")
)


class TransactionModel(Model):
    type: SmallIntegerField = SmallIntegerField()
    date: DateField = DateField()
    card_number: CharField = CharField()
    national_id: CharField = CharField()
    hour: TimeField = TimeField()
    store_name: CharField = CharField()
    store_owner: CharField = CharField()
    amount: DecimalField = DecimalField(max_digits=10, decimal_places=2)

    created_at: DateTimeField = DateTimeField()
    updated_at: DateTimeField = DateTimeField(null=True)

    class Meta:
        database = session


session.connect()
