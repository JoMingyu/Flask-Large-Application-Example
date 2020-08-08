import os


class LocalLevelConfig:
    ENV = "development"
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "85c145a16bd6f6e1f3e104ca78c6a102")


class ProductionLevelConfig:
    ENV = "production"
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
