import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = (os.environ.get('SECRET_KEY') or
                  'mqQAxNytzcix3m8matgPi2mBfF+dcVMCyFs@kMYtcw[pyVMzCU')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECURITY_POST_LOGIN_VIEW = 'admin/'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''


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

    'default': DevelopmentConfig
}
