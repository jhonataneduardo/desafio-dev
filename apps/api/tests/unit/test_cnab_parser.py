import pytest
from datetime import date, time

from domain.entities import EntityTransaction, TypeTransaction
from domain.exceptions import InvalidFileContentException
from infrastructure.parsers import Cnab80Parser


class TestCnab80Parser:

    @pytest.fixture
    def parser(self):
        return Cnab80Parser()

    def test_parse_single_valid_line(self, parser, cnab_valid_content):
        result = parser.parse(cnab_valid_content)
        assert len(result) == 1

        txn = result[0]
        assert txn.type == TypeTransaction.FINANCIAMENTO.value
        assert txn.date == date(2019, 3, 1)
        assert txn.amount == 142.0
        assert txn.national_id == "09620676017"
        assert txn.card_number == "4753****3153"
        assert txn.hour == time(15, 34, 53)
        assert txn.store_owner == "JOAO MACEDO"
        assert txn.store_name == "BAR DO JOAO CENTRO"

    def test_parse_multiple_lines(self, parser, cnab_multiple_lines):
        result = parser.parse(cnab_multiple_lines)
        assert len(result) == 2

        assert result[0].type == TypeTransaction.FINANCIAMENTO.value
        assert result[1].type == TypeTransaction.RECEBIMENTO_EMPRESTIMO.value

    def test_parse_amount_is_divided_by_100(self, parser, cnab_valid_content):
        result = parser.parse(cnab_valid_content)
        assert result[0].amount == 142.0

    def test_parse_strips_whitespace_from_fields(self, parser, cnab_valid_content):
        result = parser.parse(cnab_valid_content)
        txn = result[0]
        assert txn.national_id == txn.national_id.strip()
        assert txn.card_number == txn.card_number.strip()
        assert txn.store_owner == txn.store_owner.strip()
        assert txn.store_name == txn.store_name.strip()

    def test_parse_extracts_correct_type(self, parser):
        """Testa que o primeiro caractere é usado como tipo da transação."""

        line = b"1201903010000010000000000000001234****5678120000OWNER NAME    STORE NAME CENTRO1"
        result = parser.parse(line)
        assert result[0].type == TypeTransaction.DEBITO.value

    def test_parse_extracts_correct_date(self, parser):
        """Testa que os caracteres 1-8 são interpretados como data (YYYYMMDD)."""

        line = b"1202406150000010000000000000001234****5678120000OWNER NAME    STORE NAME CENTRO1"
        result = parser.parse(line)
        assert result[0].date == date(2024, 6, 15)

    def test_parse_second_line_data(self, parser, cnab_multiple_lines):
        result = parser.parse(cnab_multiple_lines)
        txn2 = result[1]
        assert txn2.amount == 132.0
        assert txn2.national_id == "55641815063"
        assert txn2.card_number == "3123****7687"
        assert txn2.hour == time(14, 56, 7)
        assert txn2.store_owner == "MARIA JOSEFINA"
        assert txn2.store_name == "LOJA DO O - CENTRO"

    def test_parse_returns_entity_transaction_instances(self, parser, cnab_valid_content):
        result = parser.parse(cnab_valid_content)
        assert all(isinstance(txn, EntityTransaction) for txn in result)

    def test_parse_all_transaction_types(self, parser):
        """Testa que todos os 9 tipos de transação são parseados corretamente."""

        base = "201903010000010000000000000001234****5678120000OWNER NAME    STORE NAME CENTRO1"
        assert len(base) == 79
        for type_val in range(1, 10):
            line = f"{type_val}{base}".encode("utf-8")
            assert len(line) == 80
            result = parser.parse(line)
            assert result[0].type == type_val

    def test_parse_empty_content_raises(self, parser):
        with pytest.raises(InvalidFileContentException, match="empty"):
            parser.parse(b"")

    def test_parse_whitespace_only_raises(self, parser):
        with pytest.raises(InvalidFileContentException, match="empty"):
            parser.parse(b"   \n  \n  ")

    def test_parse_short_line_raises(self, parser):
        with pytest.raises(InvalidFileContentException, match="expected at least 80"):
            parser.parse(b"3201903010000014200")

    def test_parse_line_with_79_chars_raises(self, parser):
        line = b"3" * 79
        assert len(line) == 79
        with pytest.raises(InvalidFileContentException, match="expected at least 80"):
            parser.parse(line)

    def test_parse_invalid_encoding_raises(self, parser):
        invalid_bytes = bytes([0x80, 0x81, 0x82] * 30)
        with pytest.raises(InvalidFileContentException, match="UTF-8"):
            parser.parse(invalid_bytes)

    def test_parse_invalid_date_raises(self, parser):
        bad_line = b"3999913010000014200096206760174753****3153153453JOAO MACEDO   BAR DO JOAO CENTRO"
        assert len(bad_line) == 80
        with pytest.raises(InvalidFileContentException, match="Error parsing line"):
            parser.parse(bad_line)

    def test_parse_type_zero_creates_entity_with_int_zero(self, parser):
        """Tipo 0 não existe no Enum, mas o parser armazena como int(line[0:1]).
        int('0') = 0 é válido, então o parser NÃO lança exceção aqui."""
        line = b"0201903010000014200096206760174753****3153153453JOAO MACEDO   BAR DO JOAO CENTRO"
        assert len(line) == 80
        result = parser.parse(line)
        assert result[0].type == 0

    def test_parse_mixed_valid_and_short_line_raises(self, parser):
        """Se uma das linhas for curta, o parser deve falhar."""
        valid = b"3201903010000014200096206760174753****3153153453JOAO MACEDO   BAR DO JOAO CENTRO"
        short = b"short"
        content = valid + b"\n" + short
        with pytest.raises(InvalidFileContentException, match="expected at least 80"):
            parser.parse(content)

    def test_parse_error_includes_line_number(self, parser):
        """Verifica que a mensagem de erro inclui o número da linha."""
        valid = b"3201903010000014200096206760174753****3153153453JOAO MACEDO   BAR DO JOAO CENTRO"
        short = b"invalid"
        content = valid + b"\n" + short
        with pytest.raises(InvalidFileContentException, match="Line 2"):
            parser.parse(content)
