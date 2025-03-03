import sys

from fastapi import HTTPException

from base.utils.my_logger import get_logger
from base.custom_enum.http_enum import HttpStatusCodeEnum, ResponseMessageEnum
logger = get_logger()


class AppServices:
    @staticmethod
    def app_response(status_code: int, message: str, success: bool = None,
                     data: any = None) -> dict:
        response = {
            "status_code": status_code,
            "success": success,
            "message": message,
            "data": data
        }

        return response

    @staticmethod
    def handle_exception(exception, is_raise=False):
        exc_type, _, tb = sys.exc_info()
        f = tb.tb_frame
        line_no, filename, function_name = \
            tb.tb_lineno, f.f_code.co_filename, f.f_code.co_name

        message = exception.detail if hasattr(exception, "detail") and bool(
            exception.detail) \
            else f"Exception type: {exc_type}, " \
                 f"Exception message: {exception.__str__()}, " \
                 f"Filename: {filename}, " \
                 f"Function name: {function_name} " \
                 f"Line number: {line_no}"

        logger.error(f"Exception error message: {message}")

        if is_raise:
            raise HTTPException(
                status_code=exception.status_code if hasattr(exception,
                                                             "status_code") else
                HttpStatusCodeEnum.INTERNAL_SERVER_ERROR.value,
                detail=ResponseMessageEnum.INTERNAL_SERVER_ERROR.value)
