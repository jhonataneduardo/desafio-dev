
from playhouse.shortcuts import model_to_dict
from peewee import Model, CharField, DecimalField, DateTimeField, SmallIntegerField, DateField, TimeField

from infrastructure.database.session import db


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
        database = db
