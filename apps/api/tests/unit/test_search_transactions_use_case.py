import pytest
from unittest.mock import Mock
from datetime import date, time

from domain.entities import EntityTransaction, TypeTransaction
from domain.repositories import TransactionRepositoryInterface
from application.dtos.input_dto import ParamsSearchTransactionsDTO
from application.usecases.search_transactions_use_case import SearchTransactionsUseCase


class TestSearchTransactionsUseCase:
    """Testes unitários para o caso de uso SearchTransactionsUseCase."""

    @pytest.fixture
    def mock_repository(self):
        return Mock(spec=TransactionRepositoryInterface)

    @pytest.fixture
    def use_case(self, mock_repository):
        return SearchTransactionsUseCase(mock_repository)

    @pytest.fixture
    def transactions_same_store(self):
        return [
            EntityTransaction(
                type=TypeTransaction.DEBITO,
                date=date(2024, 3, 1),
                card_number="4753****3153",
                national_id="09620676017",
                hour=time(15, 34, 53),
                store_name="BAR DO JOAO",
                store_owner="JOAO MACEDO",
                amount=142.0,
            ),
            EntityTransaction(
                type=TypeTransaction.CREDITO,
                date=date(2024, 3, 2),
                card_number="4753****3153",
                national_id="09620676017",
                hour=time(10, 0, 0),
                store_name="BAR DO JOAO",
                store_owner="JOAO MACEDO",
                amount=250.0,
            ),
        ]

    @pytest.fixture
    def transactions_multiple_stores(self):
        return [
            EntityTransaction(
                type=TypeTransaction.DEBITO,
                date=date(2024, 3, 1),
                card_number="4753****3153",
                national_id="09620676017",
                hour=time(15, 34, 53),
                store_name="BAR DO JOAO",
                store_owner="JOAO MACEDO",
                amount=142.0,
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
            ),
            EntityTransaction(
                type=TypeTransaction.BOLETO,
                date=date(2024, 3, 3),
                card_number="4753****3153",
                national_id="09620676017",
                hour=time(8, 30, 0),
                store_name="BAR DO JOAO",
                store_owner="JOAO MACEDO",
                amount=50.0,
            ),
        ]

    def test_initialization(self, mock_repository):
        use_case = SearchTransactionsUseCase(mock_repository)
        assert use_case.transaction_repository is mock_repository

    def test_execute_without_group_by_returns_list(
        self, use_case, mock_repository, sample_transactions
    ):
        params = ParamsSearchTransactionsDTO(group_by=None)
        mock_repository.find_all.return_value = sample_transactions

        result = use_case.execute(params)

        assert isinstance(result, list)
        assert len(result) == 2
        mock_repository.find_all.assert_called_once_with(params)

    def test_execute_with_group_by_store_returns_dict(
        self, use_case, mock_repository, transactions_multiple_stores
    ):
        params = ParamsSearchTransactionsDTO(group_by="store")
        mock_repository.find_all.return_value = transactions_multiple_stores

        result = use_case.execute(params)

        assert isinstance(result, dict)
        assert "BAR DO JOAO" in result
        assert "LOJA CENTRAL" in result

    def test_execute_with_group_by_store_groups_correctly(
        self, use_case, mock_repository, transactions_multiple_stores
    ):
        params = ParamsSearchTransactionsDTO(group_by="store")
        mock_repository.find_all.return_value = transactions_multiple_stores

        result = use_case.execute(params)

        assert len(result["BAR DO JOAO"]) == 2
        assert len(result["LOJA CENTRAL"]) == 1

    def test_execute_with_group_by_store_single_store(
        self, use_case, mock_repository, transactions_same_store
    ):
        params = ParamsSearchTransactionsDTO(group_by="store")
        mock_repository.find_all.return_value = transactions_same_store

        result = use_case.execute(params)

        assert len(result) == 1
        assert "BAR DO JOAO" in result
        assert len(result["BAR DO JOAO"]) == 2

    def test_execute_with_empty_result(self, use_case, mock_repository):
        params = ParamsSearchTransactionsDTO(group_by=None)
        mock_repository.find_all.return_value = []

        result = use_case.execute(params)

        assert result == []

    def test_execute_with_group_by_store_empty_result(self, use_case, mock_repository):
        params = ParamsSearchTransactionsDTO(group_by="store")
        mock_repository.find_all.return_value = []

        result = use_case.execute(params)

        assert isinstance(result, dict)
        assert len(result) == 0

    def test_execute_propagates_repository_exception(self, use_case, mock_repository):
        params = ParamsSearchTransactionsDTO(group_by=None)
        mock_repository.find_all.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            use_case.execute(params)
