from app import create_app
from config.app_config import ProductionLevelConfig
from config.db_config import RemoteDBConfig

application = create_app(ProductionLevelConfig, RemoteDBConfig)
