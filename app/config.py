import os
BASE_DIR = os.path.dirname(__file__)


class BaseConfig(object):
    """默认配置"""
    DEBUG = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SITE_NAME = 'CC Blog'
    ADMIN = dict(
        username='admin',
        email='admin@cc.com',
        password='admin'
    )
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    TOPICS = ['随笔', 'Python', '其他']


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        BASE_DIR, 'database', 'development.db')


class ProductionConfig(BaseConfig):
    """ 成产环境配置 """
    DEBUG = False


class TestingConfig(object):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        BASE_DIR, 'database', 'testing.db')


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
