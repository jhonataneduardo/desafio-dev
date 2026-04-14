import pytest
from datetime import date, time, datetime

from domain.entities import EntityTransaction, TypeTransaction


class TestTypeTransaction:
    """Testes para o Enum TypeTransaction."""

    def test_all_types_have_correct_values(self):
        assert TypeTransaction.DEBITO.value == 1
        assert TypeTransaction.BOLETO.value == 2
        assert TypeTransaction.FINANCIAMENTO.value == 3
        assert TypeTransaction.CREDITO.value == 4
        assert TypeTransaction.RECEBIMENTO_EMPRESTIMO.value == 5
        assert TypeTransaction.VENDAS.value == 6
        assert TypeTransaction.TED.value == 7
        assert TypeTransaction.DOC.value == 8
        assert TypeTransaction.ALUGUEL.value == 9

    def test_from_value_returns_correct_type(self):
        assert TypeTransaction.from_value(1) == TypeTransaction.DEBITO
        assert TypeTransaction.from_value(4) == TypeTransaction.CREDITO
        assert TypeTransaction.from_value(9) == TypeTransaction.ALUGUEL

    def test_from_value_raises_for_invalid_value(self):
        with pytest.raises(ValueError):
            TypeTransaction.from_value(99)

    def test_from_value_raises_for_zero(self):
        with pytest.raises(ValueError):
            TypeTransaction.from_value(0)

    def test_from_value_raises_for_negative(self):
        with pytest.raises(ValueError):
            TypeTransaction.from_value(-1)

    def test_enum_has_exactly_9_members(self):
        assert len(TypeTransaction) == 9


class TestEntityBase:
    """Testes para os campos herdados de EntityBase."""

    def test_default_id_is_none(self):
        entity = EntityTransaction(
            type=TypeTransaction.DEBITO,
            date=date(2024, 6, 1),
            card_number="1234****5678",
            national_id="12345678900",
            hour=time(14, 30),
            store_name="Loja Teste",
            store_owner="João Silva",
            amount=100.0,
        )
        assert entity.id is None

    def test_default_created_at_is_set(self):
        entity = EntityTransaction(
            type=TypeTransaction.DEBITO,
            date=date(2024, 6, 1),
            card_number="1234****5678",
            national_id="12345678900",
            hour=time(14, 30),
            store_name="Loja Teste",
            store_owner="João Silva",
            amount=100.0,
        )
        assert isinstance(entity.created_at, datetime)

    def test_default_updated_at_is_none(self):
        entity = EntityTransaction(
            type=TypeTransaction.DEBITO,
            date=date(2024, 6, 1),
            card_number="1234****5678",
            national_id="12345678900",
            hour=time(14, 30),
            store_name="Loja Teste",
            store_owner="João Silva",
            amount=100.0,
        )
        assert entity.updated_at is None

    def test_custom_id_is_preserved(self):
        entity = EntityTransaction(
            id=42,
            type=TypeTransaction.DEBITO,
            date=date(2024, 6, 1),
            card_number="1234****5678",
            national_id="12345678900",
            hour=time(14, 30),
            store_name="Loja Teste",
            store_owner="João Silva",
            amount=100.0,
        )
        assert entity.id == 42


class TestEntityTransaction:
    """Testes para a entidade EntityTransaction."""

    def test_creation_with_all_fields(self, sample_transaction):
        assert sample_transaction.type == TypeTransaction.DEBITO
        assert sample_transaction.date == date(2024, 3, 1)
        assert sample_transaction.card_number == "4753****3153"
        assert sample_transaction.national_id == "09620676017"
        assert sample_transaction.hour == time(15, 34, 53)
        assert sample_transaction.store_name == "BAR DO JOAO"
        assert sample_transaction.store_owner == "JOAO MACEDO"
        assert sample_transaction.amount == 142.0

    def test_to_dict_returns_all_fields(self, sample_transaction):
        result = sample_transaction.to_dict()
        assert isinstance(result, dict)
        assert result["type"] == TypeTransaction.DEBITO
        assert result["date"] == date(2024, 3, 1)
        assert result["card_number"] == "4753****3153"
        assert result["national_id"] == "09620676017"
        assert result["hour"] == time(15, 34, 53)
        assert result["store_name"] == "BAR DO JOAO"
        assert result["store_owner"] == "JOAO MACEDO"
        assert result["amount"] == 142.0

    def test_to_dict_includes_base_fields(self, sample_transaction):
        result = sample_transaction.to_dict()
        assert "id" in result
        assert "created_at" in result
        assert "updated_at" in result

    def test_from_dict_creates_valid_entity(self):
        data = {
            "type": 4,
            "date": date(2024, 6, 1),
            "card_number": "9876****1234",
            "national_id": "98765432100",
            "hour": time(16, 45),
            "store_name": "Outra Loja",
            "store_owner": "Maria Santos",
            "amount": 250.0,
        }
        entity = EntityTransaction.from_dict(data)
        assert entity.type == 4
        assert entity.store_owner == "Maria Santos"
        assert entity.amount == 250.0

    def test_from_dict_with_all_types(self):
        """Testa criação de entidade com cada tipo de transação."""
        for type_val in range(1, 10):
            data = {
                "type": type_val,
                "date": date(2024, 1, 1),
                "card_number": "0000****0000",
                "national_id": "00000000000",
                "hour": time(0, 0, 0),
                "store_name": "Loja",
                "store_owner": "Dono",
                "amount": 0.0,
            }
            entity = EntityTransaction.from_dict(data)
            assert entity.type == type_val

    def test_amount_preserves_decimal_precision(self):
        entity = EntityTransaction(
            type=TypeTransaction.CREDITO,
            date=date(2024, 1, 1),
            card_number="0000****0000",
            national_id="00000000000",
            hour=time(0, 0),
            store_name="Loja",
            store_owner="Dono",
            amount=150.75,
        )
        assert entity.amount == 150.75

    def test_amount_zero(self):
        entity = EntityTransaction(
            type=TypeTransaction.CREDITO,
            date=date(2024, 1, 1),
            card_number="0000****0000",
            national_id="00000000000",
            hour=time(0, 0),
            store_name="Loja",
            store_owner="Dono",
            amount=0.0,
        )
        assert entity.amount == 0.0
