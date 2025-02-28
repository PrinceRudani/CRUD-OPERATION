from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import redirect, request

from base.config.static_variables import StaticVariables
from base.utils.my_logger import get_logger

static_variables = StaticVariables()
logger = get_logger()


class LoginService:
    @staticmethod
    def generate_token(user_id, user_email, user_role):
        try:
            access_token_payload = {
                "exp": datetime.utcnow() + timedelta(
                    minutes=int(static_variables.ACCESS_TOKEN_EXPIRE_MINUTES)),
                "iat": datetime.utcnow(),
                "user_id": user_id,
                "user_email": user_email,
                "user_role": user_role
            }

            logger.debug(
                f"Creating access token with payload: {access_token_payload}")
            logger.info("Access token payload created successfully")

            access_token = jwt.encode(access_token_payload,
                                      static_variables.JWT_SECRET_KEY,
                                      algorithm=static_variables.JWT_ALGORITHM)

            refresh_token_payload = {
                "exp": datetime.utcnow() + timedelta(minutes=int(
                    static_variables.REFRESH_TOKEN_EXPIRE_MINUTES)),
                "iat": datetime.utcnow(),
                "user_id": user_id,
                "user_email": user_email,
                "user_role": user_role
            }

            refresh_token = jwt.encode(refresh_token_payload,
                                       static_variables.JWT_SECRET_KEY,
                                       algorithm=static_variables.JWT_ALGORITHM)

            return access_token, refresh_token

        except Exception as e:
            logger.error(f"Error generating tokens: {str(e)}")
            return redirect('/login?error=token_generation_failed')

    @staticmethod
    def refresh_token(request, fn):
        try:
            refresh_token = request.cookies.get(
                static_variables.TOKEN_REFRESH_KEY)

            if refresh_token is None:
                return redirect(
                    '/login?error=no_refresh_token')

            try:
                data = jwt.decode(refresh_token,
                                  static_variables.JWT_SECRET_KEY,
                                  algorithms=[static_variables.JWT_ALGORITHM])
                logger.debug(f"Decoded refresh token data: {data}")
                logger.info("Refresh token successfully validated")
            except jwt.ExpiredSignatureError:
                logger.warning("Refresh token expired.")
                return redirect('/login?error=refresh_token_expired')

            logger.info("Generating new tokens from refresh token")
            new_access_token, new_refresh_token = LoginService.generate_token(
                data['user_id'], data['user_email'], data['user_role'])
            logger.info("New tokens generated successfully")
            response = fn()
            response.set_cookie(static_variables.TOKEN_ACCESS_KEY,
                                new_access_token, max_age=int(
                    static_variables.ACCESS_TOKEN_EXPIRE_MINUTES) * 60,
                                httponly=True)
            response.set_cookie(static_variables.TOKEN_REFRESH_KEY,
                                new_refresh_token, max_age=int(
                    static_variables.REFRESH_TOKEN_EXPIRE_MINUTES) * 60,
                                httponly=True)
            return response

        except Exception as ex:
            logger.error(f"Error refreshing token: {str(ex)}")
            return redirect('/login?error=refresh_failed')

    @staticmethod
    def login_required(role):
        def inner(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                access_token = request.cookies.get(
                    static_variables.TOKEN_ACCESS_KEY)
                if access_token is None:
                    return redirect('/login?error=no_access_token')

                try:
                    data = jwt.decode(access_token,
                                      static_variables.JWT_SECRET_KEY,
                                      algorithms=[static_variables.JWT_ALGORITHM])

                    logger.debug(f"Decoded access token data: {data}")
                    logger.info("Access token successfully validated")

                    if data['user_role'] != role:
                        return redirect(
                            '/unauthorized?error=invalid_role')

                    return fn(*args, **kwargs)
                except Exception as ex:
                    logger.error(f"Error during access control: {str(ex)}")
                    return redirect('/login?error=auth_failed')

            return decorator

        return inner
