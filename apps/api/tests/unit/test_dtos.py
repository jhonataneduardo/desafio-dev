from application.dtos import InputTransactionDTO


def test_input_transaction_dto():

    dto = InputTransactionDTO(
        type=1,
        date="2024-06-01",
        card_number="1234-5678-9012-3456",
        national_id="12345678900",
        hour="12:00:00",
        store_name="Test Store",
        store_owner="John Doe",
        amount=100.0
    )

    assert dto.type == 1
    assert dto.date == "2024-06-01"
    assert dto.card_number == "1234-5678-9012-3456"
    assert dto.national_id == "12345678900"
    assert dto.hour == "12:00:00"
    assert dto.store_name == "Test Store"
    assert dto.store_owner == "John Doe"
    assert dto.amount == 100.0
    
def test_input_transaction_dto_to_dict():

    dto = InputTransactionDTO(
        type=1,
        date="2024-06-01",
        card_number="1234-5678-9012-3456",
        national_id="12345678900",
        hour="12:00:00",
        store_name="Test Store",
        store_owner="John Doe",
        amount=100.0
    )

    dto_dict = dto.to_dict()
    assert dto_dict["type"] == 1
    assert dto_dict["date"] == "2024-06-01"
    assert dto_dict["card_number"] == "1234-5678-9012-3456"
    assert dto_dict["national_id"] == "12345678900"
    assert dto_dict["hour"] == "12:00:00"
    assert dto_dict["store_name"] == "Test Store"
    assert dto_dict["store_owner"] == "John Doe"
    assert dto_dict["amount"] == 100.0