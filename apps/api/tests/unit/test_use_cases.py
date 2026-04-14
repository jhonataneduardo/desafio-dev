import pytest
from unittest.mock import Mock

from domain.entities import EntityTransaction, TypeTransaction
from domain.parsers import CnabParserInterface
from domain.repositories import TransactionRepositoryInterface
from domain.exceptions import InvalidFileContentException
from application.usecases.process_cnab_use_case import ProcessCnabFileUseCase


class TestProcessCnabFileUseCase:
    """Testes unitários para o caso de uso ProcessCnabFileUseCase."""

    @pytest.fixture
    def mock_parser(self):
        return Mock(spec=CnabParserInterface)

    @pytest.fixture
    def mock_repository(self):
        return Mock(spec=TransactionRepositoryInterface)

    @pytest.fixture
    def use_case(self, mock_parser, mock_repository):
        return ProcessCnabFileUseCase(mock_parser, mock_repository)

    def test_initialization(self, mock_parser, mock_repository):
        use_case = ProcessCnabFileUseCase(mock_parser, mock_repository)
        assert use_case.cnab_parser is mock_parser
        assert use_case.transaction_repository is mock_repository

    def test_execute_calls_parser_with_content(
        self, use_case, mock_parser, mock_repository
    ):
        content = b"fake cnab content"
        mock_parser.parse.return_value = []
        mock_repository.save_batch.return_value = []

        use_case.execute(content)

        mock_parser.parse.assert_called_once_with(content)

    def test_execute_calls_repository_save_batch_with_parsed_transactions(
        self, use_case, mock_parser, mock_repository, sample_transactions
    ):
        content = b"fake cnab content"
        mock_parser.parse.return_value = sample_transactions
        mock_repository.save_batch.return_value = sample_transactions

        use_case.execute(content)

        mock_repository.save_batch.assert_called_once_with(sample_transactions)

    def test_execute_returns_saved_transactions(
        self, use_case, mock_parser, mock_repository, sample_transactions
    ):
        content = b"fake cnab content"
        mock_parser.parse.return_value = sample_transactions
        mock_repository.save_batch.return_value = sample_transactions

        result = use_case.execute(content)

        assert result == sample_transactions
        assert len(result) == 2

    def test_execute_with_empty_parse_result(
        self, use_case, mock_parser, mock_repository
    ):
        content = b""
        mock_parser.parse.return_value = []
        mock_repository.save_batch.return_value = []

        result = use_case.execute(content)

        assert result == []
        mock_repository.save_batch.assert_called_once_with([])

    def test_execute_propagates_parser_exception(
        self, use_case, mock_parser, mock_repository
    ):
        content = b"invalid"
        mock_parser.parse.side_effect = InvalidFileContentException("CNAB file is empty")

        with pytest.raises(InvalidFileContentException, match="CNAB file is empty"):
            use_case.execute(content)

        mock_repository.save_batch.assert_not_called()

    def test_execute_propagates_repository_exception(
        self, use_case, mock_parser, mock_repository, sample_transactions
    ):
        content = b"valid content"
        mock_parser.parse.return_value = sample_transactions
        mock_repository.save_batch.side_effect = Exception("Database error")

        with pytest.raises(Exception, match="Database error"):
            use_case.execute(content)

    def test_execute_does_not_call_save_individually(
        self, use_case, mock_parser, mock_repository, sample_transactions
    ):
        """Verifica que o use case usa save_batch, não save individual."""
        content = b"content"
        mock_parser.parse.return_value = sample_transactions
        mock_repository.save_batch.return_value = sample_transactions

        use_case.execute(content)

        mock_repository.save.assert_not_called()
        mock_repository.save_batch.assert_called_once()
