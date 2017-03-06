# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
import logging 
import os

from celery import Celery
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from raven.contrib.celery import register_signal, register_logger_signal
from google.cloud import storage
from google.oauth2 import service_account
from werkzeug.contrib.fixers import ProxyFix

from config import config, Config

bootstrap = Bootstrap()
db = SQLAlchemy()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
sentry = Sentry()

logging_map = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def storage_client_bucket(app):
    """
    Given app returns the client and bucket for Google Storage
    """
    ACCOUNT_JSON_PATH = app.config.get('GOOGLE_JSON_PATH')
    GOOGLE_PROJECT = app.config.get('GOOGLE_PROJECT')
    BUCKET = app.config.get('STORAGE_CONTAINER')

    credentials = service_account.Credentials.from_service_account_file(ACCOUNT_JSON_PATH)
    client = storage.Client(project=GOOGLE_PROJECT, credentials=credentials)
    bucket = client.get_bucket(BUCKET)

    return client, bucket

TaskBase = celery.Task


class ContextTask(TaskBase):
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db.session.remove()

celery.Task = ContextTask


def create_app(config_name):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    '''
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging_map[log_level])
    stream = logging.StreamHandler()
    stream.setLevel(logging_map[log_level])
    logger.addHandler(stream)


    if config_name in ('docker', 'development', 'production'):
        sentry.init_app(app, logging=True, level=logging.INFO)
        app.wsgi_app = ProxyFix(app.wsgi_app)

    bootstrap.init_app(app)
    db.init_app(app)
    celery.conf.update(app.config)

    from underground_garage.main import main
    app.register_blueprint(main)

    return app

import underground_garage.models
