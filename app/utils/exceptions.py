class APIError(Exception):
    """Кастомная ошибка API."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

def handle_api_error(error: APIError) -> tuple[dict, int]:
    """Обработчик ошибок для Flask."""
    return {"error": error.message}, error.status_code