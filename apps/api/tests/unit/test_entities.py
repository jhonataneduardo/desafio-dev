from datetime import datetime, date, time

from domain.entities import EntityTransaction, TypeTransaction


def test_simples_entity_base():
    entity = EntityTransaction(
        type=TypeTransaction.DEBITO,
        date=date(2024, 6, 1),
        card_number="1234-5678-9012-3456",
        national_id="123.456.789-00",
        hour=time(14, 30),
        store_name="Loja Teste",
        store_owner="João Silva",
        amount=100.0
    )
    assert entity.id is None
    assert isinstance(entity.created_at, datetime)
    assert entity.updated_at is None


def test_simple_entity_transaction():
    transaction = EntityTransaction(
        type=TypeTransaction.DEBITO,
        date=date(2024, 6, 1),
        card_number="1234-5678-9012-3456",
        national_id="123.456.789-00",
        hour=time(14, 30),
        store_name="Loja Teste",
        store_owner="João Silva",
        amount=100.0
    )
    assert transaction.type == TypeTransaction.DEBITO
    assert transaction.date == date(2024, 6, 1)
    assert transaction.card_number == "1234-5678-9012-3456"
    assert transaction.national_id == "123.456.789-00"
    assert transaction.hour == time(14, 30)
    assert transaction.store_name == "Loja Teste"
    assert transaction.store_owner == "João Silva"
    assert transaction.amount == 100.0
    assert transaction.updated_at is None
    
    
    
def test_entity_transaction_to_dict():    
    transaction = EntityTransaction(
        type=TypeTransaction.DEBITO,
        date=date(2024, 6, 1),
        card_number="1234-5678-9012-3456",
        national_id="123.456.789-00",
        hour=time(14, 30),
        store_name="Loja Teste",
        store_owner="João Silva",
        amount=100.0
    )
    
    transaction_dict = transaction.to_dict()
    assert transaction_dict["type"] == TypeTransaction.DEBITO
    assert transaction_dict["date"] == date(2024, 6, 1)
    assert transaction_dict["card_number"] == "1234-5678-9012-3456"
    assert transaction_dict["national_id"] == "123.456.789-00"
    assert transaction_dict["hour"] == time(14, 30)
    assert transaction_dict["store_name"] == "Loja Teste"
    assert transaction_dict["store_owner"] == "João Silva"
    assert transaction_dict["amount"] == 100.0

def test_entity_transaction():
    transaction = EntityTransaction(
        type=TypeTransaction.CREDITO,
        date=date(2024, 6, 1),
        card_number="9876-5432-1098-7654",
        national_id="987.654.321-00",
        hour=time(16, 45),
        store_name="Loja Teste",
        store_owner="João Silva",
        amount=250.0
    )
    
    assert transaction.type == TypeTransaction.CREDITO
    assert transaction.date == date(2024, 6, 1)
    assert transaction.card_number == "9876-5432-1098-7654"
    assert transaction.national_id == "987.654.321-00"
    assert transaction.hour == time(16, 45)
    assert transaction.store_name == "Loja Teste"
    assert transaction.store_owner == "João Silva"
    assert transaction.amount == 250.0