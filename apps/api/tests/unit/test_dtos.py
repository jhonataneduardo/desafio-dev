import pytest
from pydantic import ValidationError

from application.dtos.input_dto import InputTransactionDTO, ParamsSearchTransactionsDTO


class TestInputTransactionDTO:
    """Testes para o DTO de entrada InputTransactionDTO."""

    @pytest.fixture
    def valid_dto_data(self):
        return {
            "type": 1,
            "date": "2024-06-01",
            "card_number": "1234****5678",
            "national_id": "12345678900",
            "hour": "14:30:00",
            "store_name": "Loja Teste",
            "store_owner": "João Silva",
            "amount": 100.50,
        }

    def test_create_valid_dto(self, valid_dto_data):
        dto = InputTransactionDTO(**valid_dto_data)
        assert dto.type == 1
        assert dto.date == "2024-06-01"
        assert dto.card_number == "1234****5678"
        assert dto.national_id == "12345678900"
        assert dto.hour == "14:30:00"
        assert dto.store_name == "Loja Teste"
        assert dto.store_owner == "João Silva"
        assert dto.amount == 100.50

    def test_id_defaults_to_none(self, valid_dto_data):
        dto = InputTransactionDTO(**valid_dto_data)
        assert dto.id is None

    def test_id_can_be_set(self, valid_dto_data):
        valid_dto_data["id"] = 42
        dto = InputTransactionDTO(**valid_dto_data)
        assert dto.id == 42

    def test_to_dict_returns_all_keys(self, valid_dto_data):
        dto = InputTransactionDTO(**valid_dto_data)
        result = dto.to_dict()
        expected_keys = {
            "id", "type", "date", "card_number", "national_id",
            "hour", "store_name", "store_owner", "amount",
        }
        assert set(result.keys()) == expected_keys

    def test_to_dict_preserves_values(self, valid_dto_data):
        dto = InputTransactionDTO(**valid_dto_data)
        result = dto.to_dict()
        assert result["type"] == 1
        assert result["date"] == "2024-06-01"
        assert result["card_number"] == "1234****5678"
        assert result["national_id"] == "12345678900"
        assert result["hour"] == "14:30:00"
        assert result["store_name"] == "Loja Teste"
        assert result["store_owner"] == "João Silva"
        assert result["amount"] == 100.50
        assert result["id"] is None

    def test_to_entity_returns_entity_transaction(self, valid_dto_data):
        dto = InputTransactionDTO(**valid_dto_data)
        entity = dto.to_entity()
        assert entity.type == 1
        assert entity.store_name == "Loja Teste"
        assert entity.amount == 100.50

    def test_missing_required_field_raises_validation_error(self):
        with pytest.raises(ValidationError):
            InputTransactionDTO(
                type=1,
                date="2024-06-01",
                # card_number omitido intencionalmente
                national_id="12345678900",
                hour="14:30:00",
                store_name="Loja",
                store_owner="Dono",
                amount=100.0,
            )

    def test_missing_amount_raises_validation_error(self):
        with pytest.raises(ValidationError):
            InputTransactionDTO(
                type=1,
                date="2024-06-01",
                card_number="1234****5678",
                national_id="12345678900",
                hour="14:30:00",
                store_name="Loja",
                store_owner="Dono",
                # amount omitido
            )

    def test_invalid_type_raises_validation_error(self):
        with pytest.raises(ValidationError):
            InputTransactionDTO(
                type="not_a_number",
                date="2024-06-01",
                card_number="1234****5678",
                national_id="12345678900",
                hour="14:30:00",
                store_name="Loja",
                store_owner="Dono",
                amount=100.0,
            )

    def test_invalid_amount_raises_validation_error(self):
        with pytest.raises(ValidationError):
            InputTransactionDTO(
                type=1,
                date="2024-06-01",
                card_number="1234****5678",
                national_id="12345678900",
                hour="14:30:00",
                store_name="Loja",
                store_owner="Dono",
                amount="not_a_number",
            )

    def test_amount_coercion_from_int(self, valid_dto_data):
        valid_dto_data["amount"] = 100
        dto = InputTransactionDTO(**valid_dto_data)
        assert dto.amount == 100.0
        assert isinstance(dto.amount, float)


class TestParamsSearchTransactionsDTO:
    """Testes para o DTO de parâmetros de busca ParamsSearchTransactionsDTO."""

    def test_create_with_group_by(self):
        dto = ParamsSearchTransactionsDTO(group_by="store")
        assert dto.group_by == "store"

    def test_group_by_defaults_to_none(self):
        dto = ParamsSearchTransactionsDTO()
        assert dto.group_by is None

    def test_to_dict_with_group_by(self):
        dto = ParamsSearchTransactionsDTO(group_by="store")
        result = dto.to_dict()
        assert result == {"group_by": "store"}

    def test_to_dict_without_group_by(self):
        dto = ParamsSearchTransactionsDTO()
        result = dto.to_dict()
        assert result == {"group_by": None}
