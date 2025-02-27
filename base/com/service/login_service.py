from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask import redirect, request, jsonify
from base.utils.my_logger import get_logger
from base.config.static_variables import StaticVariables

static_variables = StaticVariables()
logger = get_logger()

class LoginService:
    @staticmethod
    def generate_token(user_id, user_email, user_role):
        try:
            # Access token payload with expiration time
            access_token_payload = {
                "exp": datetime.utcnow() + timedelta(minutes=int(static_variables.ACCESS_TOKEN_EXPIRE_MINUTES)),
                "iat": datetime.utcnow(),
                "user_id": user_id,
                "user_email": user_email,
                "user_role": user_role
            }

            logger.info(f"Login service access token payload: {access_token_payload}")

            access_token = jwt.encode(access_token_payload, static_variables.JWT_SECRET_KEY, algorithm=static_variables.ALGORITHM)

            # Refresh token payload with expiration time
            refresh_token_payload = {
                "exp": datetime.utcnow() + timedelta(minutes=int(static_variables.REFRESH_TOKEN_EXPIRE_MINUTES)),
                "iat": datetime.utcnow(),
                "user_id": user_id,
                "user_email": user_email,
                "user_role": user_role
            }

            refresh_token = jwt.encode(refresh_token_payload, static_variables.JWT_SECRET_KEY, algorithm=static_variables.ALGORITHM)

            return access_token, refresh_token

        except Exception as e:
            logger.error(f"Error generating tokens: {str(e)}")
            raise e

    @staticmethod
    def refresh_token(request, fn):
        try:
            refresh_token = request.cookies.get(static_variables.TOKEN_REFRESH_KEY)

            if refresh_token is None:
                return redirect('/')

            data = jwt.decode(refresh_token, static_variables.JWT_SECRET_KEY, algorithms=[static_variables.ALGORITHM])

            new_access_token, new_refresh_token = LoginService.generate_token(data['user_id'], data['user_email'], data['user_role'])

            response = fn()  # Call the view function
            response.set_cookie(static_variables.TOKEN_ACCESS_KEY, new_access_token, max_age=int(static_variables.ACCESS_TOKEN_EXPIRE_MINUTES) * 60, httponly=True)
            response.set_cookie(static_variables.TOKEN_REFRESH_KEY, new_refresh_token, max_age=int(static_variables.REFRESH_TOKEN_EXPIRE_MINUTES) * 60, httponly=True)

            return response

        except Exception as ex:
            logger.error(f"Error refreshing token: {str(ex)}")
            return redirect('/')

    @staticmethod
    def login_required(role):
        def inner(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):  # No need to explicitly pass `request`
                try:
                    access_token = request.cookies.get(static_variables.TOKEN_ACCESS_KEY)

                    if access_token is None:
                        return LoginService.refresh_token(request, fn)

                    try:
                        data = jwt.decode(access_token, static_variables.JWT_SECRET_KEY, algorithms=[static_variables.ALGORITHM])

                        if data['user_role'] == role:
                            return fn(*args, **kwargs)  # Call the view function
                        else:
                            return redirect('/')

                    except jwt.ExpiredSignatureError:
                        logger.warning(f"Access token expired for {request.cookies.get(static_variables.TOKEN_ACCESS_KEY)}")
                        return redirect('/')

                except Exception as ex:
                    logger.error(f"Error during role-based access control: {str(ex)}")
                    return redirect('/')

            return decorator
        return inner
