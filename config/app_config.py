import os


class LocalLevelConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')


class ProductionLevelConfig:
    if 'SECRET_KEY' not in os.environ:
        raise AssertionError('The secret key must be passed by the <SECRET_KEY> envvar.')

    SECRET_KEY = os.environ['SECRET_KEY']
