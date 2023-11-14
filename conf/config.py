from src import FLASK_INFO


class BasicConfig(object):
    """基本設定

    [配置管理](https://dormousehole.readthedocs.io/en/latest/config.html)

    Args:
        object (_type_): _description_

    Returns:
        _type_: _description_
    """    """Base config, uses staging database server."""
    SECRET_KEY = FLASK_INFO.get('SECRET_KEY', 'SECRET_KEY')
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = True


class ProductionConfig(BasicConfig):
    DB_SERVER = FLASK_INFO.get('DB_SERVER', '192.168.19.32')


class DevelopmentConfig(BasicConfig):
    DB_SERVER = FLASK_INFO.get('DB_SERVER', 'localhost')


class TestingConfig(BasicConfig):
    """測試

    Args:
        BasicConfig (_type_): _description_
    """
    TESTING = FLASK_INFO.get('TESTING', False)
    DEBUG = FLASK_INFO.get('DEBUG', False)
    DB_SERVER = FLASK_INFO.get('DB_SERVER', 'localhost')
    DATABASE_URI = FLASK_INFO.get('DATABASE_URI', 'sqlite:///:memory:')
