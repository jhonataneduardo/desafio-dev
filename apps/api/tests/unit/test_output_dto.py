import pytest
from datetime import date, time, datetime

from domain.entities import EntityTransaction, TypeTransaction
from application.dtos.output_dto import OutputTransactionDTO


class TestOutputTransactionDTO:
    """Testes para o DTO de saída OutputTransactionDTO."""

    @pytest.fixture
    def entity_with_id(self):
        return EntityTransaction(
            id=1,
            type=TypeTransaction.CREDITO,
            date=date(2024, 3, 1),
            card_number="4753****3153",
            national_id="09620676017",
            hour=time(15, 34, 53),
            store_name="BAR DO JOAO",
            store_owner="JOAO MACEDO",
            amount=142.0,
            created_at=datetime(2024, 3, 1, 15, 34, 53),
        )

    @pytest.fixture
    def entity_with_updated_at(self):
        return EntityTransaction(
            id=2,
            type=TypeTransaction.BOLETO,
            date=date(2024, 5, 15),
            card_number="9876****5432",
            national_id="98765432100",
            hour=time(10, 0, 0),
            store_name="LOJA CENTRAL",
            store_owner="MARIA SILVA",
            amount=250.50,
            created_at=datetime(2024, 5, 15, 10, 0, 0),
            updated_at=datetime(2024, 5, 16, 12, 0, 0),
        )

    def test_model_validate_from_entity(self, entity_with_id):
        dto = OutputTransactionDTO.model_validate_from_entity(entity_with_id)
        assert dto.id == 1
        assert dto.type == TypeTransaction.CREDITO.value
        assert dto.date == date(2024, 3, 1)
        assert dto.card_number == "4753****3153"
        assert dto.national_id == "09620676017"
        assert dto.hour == time(15, 34, 53)
        assert dto.store_name == "BAR DO JOAO"
        assert dto.store_owner == "JOAO MACEDO"
        assert dto.amount == 142.0

    def test_updated_at_defaults_to_none(self, entity_with_id):
        dto = OutputTransactionDTO.model_validate_from_entity(entity_with_id)
        assert dto.updated_at is None

    def test_updated_at_is_preserved_when_set(self, entity_with_updated_at):
        dto = OutputTransactionDTO.model_validate_from_entity(
            entity_with_updated_at)
        assert dto.updated_at == datetime(2024, 5, 16, 12, 0, 0)

    def test_created_at_is_preserved(self, entity_with_id):
        dto = OutputTransactionDTO.model_validate_from_entity(entity_with_id)
        assert dto.created_at == datetime(2024, 3, 1, 15, 34, 53)

    def test_serialization_to_json_mode(self, entity_with_id):
        dto = OutputTransactionDTO.model_validate_from_entity(entity_with_id)
        json_data = dto.model_dump(mode="json")
        assert isinstance(json_data, dict)
        assert isinstance(json_data["date"], str)
        assert isinstance(json_data["hour"], str)
        assert isinstance(json_data["created_at"], str)

    def test_serialization_includes_all_fields(self, entity_with_id):
        dto = OutputTransactionDTO.model_validate_from_entity(entity_with_id)
        json_data = dto.model_dump(mode="json")
        expected_keys = {
            "id", "type", "date", "card_number", "national_id",
            "hour", "store_name", "store_owner", "amount",
            "created_at", "updated_at",
        }
        assert set(json_data.keys()) == expected_keys

    def test_amount_is_float(self, entity_with_id):
        dto = OutputTransactionDTO.model_validate_from_entity(entity_with_id)
        assert isinstance(dto.amount, float)
