from unittest.mock import Mock
from application.use_cases import ImportTrasactionsUseCase


def test_import_use_case():
    transaction_repository = Mock()
    use_case = ImportTrasactionsUseCase(transaction_repository)
    assert use_case is not None


def test_import_use_case_execute():
    transaction_repository = Mock()
    use_case = ImportTrasactionsUseCase(transaction_repository)

    input_transactions = [
        Mock(),
        Mock(),
        Mock()
    ]

    use_case.execute(input_transactions)

    assert transaction_repository.save.call_count == 3
    transaction_repository.save.assert_any_call(input_transactions[0])
    transaction_repository.save.assert_any_call(input_transactions[1])
    transaction_repository.save.assert_any_call(input_transactions[2])
