import os


class LocalLevelConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')


class ProductionLevelConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
