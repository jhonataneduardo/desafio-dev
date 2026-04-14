import pytest
from datetime import date, time, datetime

from domain.entities import EntityTransaction, TypeTransaction
from infrastructure.repositories.transaction_repository import TransactionRepository


class TestTransactionRepositoryIntegration:
    """Testes de integração do TransactionRepository com banco de dados real (SQLite)."""

    @pytest.fixture
    def repository(self, test_session):
        return TransactionRepository(db=test_session)

    @pytest.fixture
    def sample_transaction(self):
        return EntityTransaction(
            type=TypeTransaction.DEBITO,
            date=date(2024, 3, 1),
            card_number="4753****3153",
            national_id="09620676017",
            hour=time(15, 34, 53),
            store_name="BAR DO JOAO",
            store_owner="JOAO MACEDO",
            amount=142.0,
            created_at=datetime.now(),
        )

    def test_save_persists_transaction(self, repository, sample_transaction):
        result = repository.save(sample_transaction)

        assert result.id is not None
        assert result.type == TypeTransaction.DEBITO
        assert result.amount == 142.0
        assert result.store_name == "BAR DO JOAO"

    def test_save_returns_entity_with_generated_id(self, repository, sample_transaction):
        result = repository.save(sample_transaction)
        assert isinstance(result.id, int)
        assert result.id > 0

    def test_save_batch_persists_multiple_transactions(self, repository):
        transactions = [
            EntityTransaction(
                type=TypeTransaction.DEBITO,
                date=date(2024, 3, 1),
                card_number="4753****3153",
                national_id="09620676017",
                hour=time(15, 34, 53),
                store_name="BAR DO JOAO",
                store_owner="JOAO MACEDO",
                amount=142.0,
                created_at=datetime.now(),
            ),
            EntityTransaction(
                type=TypeTransaction.CREDITO,
                date=date(2024, 3, 2),
                card_number="1234****5678",
                national_id="12345678900",
                hour=time(10, 0, 0),
                store_name="LOJA CENTRAL",
                store_owner="MARIA SILVA",
                amount=250.0,
                created_at=datetime.now(),
            ),
        ]

        result = repository.save_batch(transactions)

        assert len(result) == 2
        assert all(t.id is not None for t in result)
        assert result[0].store_name == "BAR DO JOAO"
        assert result[1].store_name == "LOJA CENTRAL"

    def test_save_batch_empty_list(self, repository):
        result = repository.save_batch([])
        assert result == []

    def test_entity_model_roundtrip_preserves_data(self, repository, sample_transaction):
        """Testa que dados sobrevivem ao ciclo Entity → Model → Entity."""
        result = repository.save(sample_transaction)

        assert result.type == sample_transaction.type
        assert result.date == sample_transaction.date
        assert result.card_number == sample_transaction.card_number
        assert result.national_id == sample_transaction.national_id
        assert result.hour == sample_transaction.hour
        assert result.store_name == sample_transaction.store_name
        assert result.store_owner == sample_transaction.store_owner
        assert float(result.amount) == sample_transaction.amount
