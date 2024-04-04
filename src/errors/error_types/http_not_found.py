class HttpNotFoundError(Exception):
    def __init__(self, message:str) -> None:
        super().__init__(message)
        self.message = message
        self.name = "Não encontrado"
        self.status_code = 404