
from enum import Enum

class HttpStatusCodeEnum(int, Enum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500


class RespondMessageEnum(str, Enum):
    USER_REGISTERED = "User registered successfully"
    USER_IS_BLOCKED = "You are not authorized to access this resource"
    USER_NOT_FOUND = "User not found"
    USER_ALREADY_EXISTS = "User already exists"
    USER_DELETED = "User deleted successfully"
    USER_UPDATED = "User updated successfully"
    USER_LOGIN_SUCCESS = "User logged in successfully"
    USER_LOGIN_FAILED = "User login failed"
    USER_LOGGED_OUT = "User logged out successfully"
    USER_PASSWORD_CHANGED = "User password changed successfully"

    GET_DATA = "data fetched successfully"
    UPDATE_DATA = "data updated successfully"
    INSERT_DATA = "data inserted successfully"
    DELETE_DATA = "data deleted successfully"

    NOT_FOUND = "Data not found"
    FILE_NOT_FOUND = "File not found"
    ID_NOT_FOUND = "ID not found"
    DUPLICATE_PDF = "PDF already exists"
    FILE_STATUS = "FIle process is currently in process, so it can't be downloaded. Please try again later."
    FILE_RESTART_STATUS = "Restart is starting now."