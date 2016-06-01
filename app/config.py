import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = (os.environ.get('SECRET_KEY') or
                  'mqQAxNytzcix3m8matgPi2mBfF+dcVMCyFs@kMYtcw[pyVMzCU')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECURITY_POST_LOGIN_VIEW = 'admin/'
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL',
                                       'redis://localhost:6379/0')
    STORAGE_PROVIDER = os.environ.get('STORAGE_PROVIDER')
    STORAGE_KEY = os.environ.get('STORAGE_KEY')
    STORAGE_SECRET = os.environ.get('STORAGE_SECRET')
    STORAGE_CONTAINER = os.environ.get('STORAGE_CONTAINER')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('UNDERGROUND_DB') or
                               'postgresql://localhost/underground_garage')


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = '1'
    CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('UNDERGROUND_DB')
    SENTRY_DSN = os.environ.get('SENTRY_DSN')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}
