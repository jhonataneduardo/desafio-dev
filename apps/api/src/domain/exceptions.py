class CnabException(Exception):
    def __init__(self, message="Erro genérico do CNAB."):
        super().__init__(message)
        self.message = message


class InvalidFileException(CnabException):
    def __init__(self, message="Invalid file."):
        super().__init__(message)
        self.message = message


class InvalidFileContentException(CnabException):
    def __init__(self, message="Invalid file content."):
        super().__init__(message)
        self.message = message
