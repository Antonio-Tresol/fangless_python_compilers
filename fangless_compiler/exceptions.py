class LexerError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class IndentationMismatchError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ParserError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
