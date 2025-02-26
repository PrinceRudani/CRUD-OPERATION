class StasticVariables:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
    JWT_SECRET_KEY = 'data'
    JWT_ACCESS_TOKEN_EXPIRES = 30
    JWT_REFRESH_TOKEN_EXPIRES = 60 * 24 * 7
    ALGORITHM = 'HS256'

config = {
    'default': StasticVariables
}