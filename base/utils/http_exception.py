from werkzeug.exceptions import HTTPException

class BaseCusException(HTTPException):
    def __init__(self, message, status_code, flash_message=None):
        self.message = message
        self.code = status_code
        self.flash_message = flash_message  # User-facing message
        super().__init__(message)

    def to_dict(self):
        return {"error": self.message, "status_code": self.code}

    def get_flash_message(self):
        return self.flash_message or "An unexpected error occurred"
