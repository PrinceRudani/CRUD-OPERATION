from datetime import datetime, timedelta
import jwt
from base.utils.MyLogger import get_logger
from base.config.ststic_variables import StsticVariables

static_variables = StsticVariables()
logger = get_logger()

class LoginService:
    @staticmethod
    def generate_token(username, access_token_expiration_minutes):
        try:
            access_token_payload = {
                "exp": datetime.utcnow() + timedelta(
                    minutes=int(access_token_expiration_minutes)),
                "username": username,
            }
            return access_token_payload
        except Exception as e:
            raise e


class AuthService:
    @staticmethod
    def get_user_by_identifier(identifier):
        pass

    @staticmethod
    def generate_token(user_id, user_email, user_role):
        try:
            # Access token payload with expiration time
            access_token_payload = {
                "exp": datetime.utcnow() + timedelta(
                    minutes=int(static_variables.ACCESS_TOKEN_EXPIRE_MINUTES)),
                "iat": datetime.utcnow(),
                "user_id": user_id,
                "user_email": user_email,
                "user_role": user_role
            }

            logger.info(
                f"Login service access token payload: {access_token_payload}")

            access_token = jwt.encode(
                access_token_payload,
                static_variables.SECRET_KEY,
                algorithm=static_variables.ALGORITHM
            )

            # Refresh token payload with expiration time
            refresh_token_payload = {
                "exp": datetime.utcnow() + timedelta(
                    minutes=int(static_variables.REFRESH_TOKEN_EXPIRE_MINUTES)),
                "iat": datetime.utcnow(),
                "user_id": user_id,
                "user_email": user_email,
                "user_role": user_role
            }

            refresh_token = jwt.encode(
                refresh_token_payload,
                static_variables.SECRET_KEY,
                algorithm=static_variables.ALGORITHM
            )

            return access_token, refresh_token

        except Exception as e:
            raise e
