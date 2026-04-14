from domain.exceptions import InvalidFileException, InvalidFileContentException


class TestInvalidFileException:
    """Testes para a exceção InvalidFileException."""

    def test_default_message(self):
        exc = InvalidFileException()
        assert exc.message == "Invalid file."
        assert str(exc) == "Invalid file."

    def test_custom_message(self):
        exc = InvalidFileException("Arquivo com formato inválido")
        assert exc.message == "Arquivo com formato inválido"
        assert str(exc) == "Arquivo com formato inválido"

    def test_is_exception_subclass(self):
        assert issubclass(InvalidFileException, Exception)

    def test_can_be_raised_and_caught(self):
        try:
            raise InvalidFileException("teste")
        except InvalidFileException as e:
            assert e.message == "teste"

    def test_can_be_caught_as_generic_exception(self):
        try:
            raise InvalidFileException()
        except Exception as e:
            assert isinstance(e, InvalidFileException)


class TestInvalidFileContentException:
    """Testes para a exceção InvalidFileContentException."""

    def test_default_message(self):
        exc = InvalidFileContentException()
        assert exc.message == "Invalid file content."
        assert str(exc) == "Invalid file content."

    def test_custom_message(self):
        exc = InvalidFileContentException("Linha 5 com 60 chars")
        assert exc.message == "Linha 5 com 60 chars"

    def test_is_exception_subclass(self):
        assert issubclass(InvalidFileContentException, Exception)

    def test_can_be_raised_and_caught(self):
        try:
            raise InvalidFileContentException("conteúdo inválido")
        except InvalidFileContentException as e:
            assert e.message == "conteúdo inválido"

    def test_can_be_caught_as_generic_exception(self):
        try:
            raise InvalidFileContentException()
        except Exception as e:
            assert isinstance(e, InvalidFileContentException)
