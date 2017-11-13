import os
import socket
from datetime import timedelta


class Config:
    HOST, PORT = socket.gethostbyname(socket.gethostname()), 3003

    SECRET_KEY = os.getenv('SECRET_KEY')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=60)
    JWT_HEADER_TYPE = 'JWT'

    API_VER = '1.0'
    API_TITLE = 'QuickStart from PlanB'
    API_DESC = '''
    # [BASE URL] http://{0}:{1}
    
    JWT Access Token의 유효기간은 {2}일, Refresh Token의 유효기간은 {3}일입니다.
    
    - Status Code 401 UNAUTHORIZED : JWT 토큰 만료됨, 또는 토큰이 정상적으로 전달되지 않음
    - Status Code 403 Forbidden : 권한 없음
    - Status Code 500 Internal Server Error : 서버 내부 오류
    '''.format(HOST, PORT, JWT_ACCESS_TOKEN_EXPIRES.days, JWT_REFRESH_TOKEN_EXPIRES.days)
    # http://flask-jwt-extended.readthedocs.io/en/latest/options.html


class DevConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'dev': DevConfig,
    'production': ProductionConfig
}
