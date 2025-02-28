from werkzeug.exceptions import HTTPException


class CustomHTTPException(HTTPException):

    def __init__(self, message="An error occurred", status_code=400):
        self.message = message
        self.code = status_code
        super().__init__(message)

    def to_dict(self):
        return {"error": self.message, "status_code": self.code}
