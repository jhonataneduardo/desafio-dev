import pytest

from domain.entities import TransactionQuery


class TestTransactionQuery:
    """Testes para o Value Object TransactionQuery."""

    def test_create_with_group_by(self):
        dto = TransactionQuery(group_by="store")
        assert dto.group_by == "store"

    def test_group_by_defaults_to_none(self):
        dto = TransactionQuery()
        assert dto.group_by is None

