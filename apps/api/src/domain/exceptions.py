class InvalidFileException(Exception):
    def __init__(self, message="Invalid file."):
        super().__init__(message)
        self.message = message


class InvalidFileContentException(Exception):
    def __init__(self, message="Invalid file content."):
        super().__init__(message)
        self.message = message
