import os

from app import create_app
from config.app_config import ProductionLevelConfig
from config.db_config import RemoteDBConfig

if "SECRET_KEY" not in os.environ:
    raise Warning("The secret key must be passed by the <SECRET_KEY> envvar.")

application = create_app(ProductionLevelConfig, RemoteDBConfig)
