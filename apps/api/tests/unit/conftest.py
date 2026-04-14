import pytest
from datetime import date, time, datetime

from domain.entities import EntityTransaction, TypeTransaction


@pytest.fixture
def cnab_valid_content() -> bytes:
    """Retorna o conteúdo de uma linha CNAB válida (80 caracteres)."""
    return (
        b"3201903010000014200096206760174753****3153153453JOAO MACEDO   BAR DO JOAO CENTRO"
    )


@pytest.fixture
def cnab_multiple_lines() -> bytes:
    """CNAB com múltiplas linhas válidas."""
    line1 = b"3201903010000014200096206760174753****3153153453JOAO MACEDO   BAR DO JOAO CENTRO"
    line2 = b"5201903010000013200556418150633123****7687145607MARIA JOSEFINALOJA DO O - CENTRO"
    return line1 + b"\n" + line2


@pytest.fixture
def sample_transaction():
    """Retorna uma EntityTransaction válida para uso em testes."""
    return EntityTransaction(
        type=TypeTransaction.DEBITO,
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
def sample_transactions():
    """Retorna uma lista de EntityTransaction para uso em testes."""
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
            type=TypeTransaction.RECEBIMENTO_EMPRESTIMO,
            date=date(2024, 3, 1),
            card_number="3123****7687",
            national_id="55641815063",
            hour=time(14, 56, 7),
            store_name="LOJA DO O - CENTRO",
            store_owner="MARIA JOSEFINA",
            amount=132.0,
        ),
    ]
