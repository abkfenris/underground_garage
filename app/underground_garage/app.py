# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from celery import Celery
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from google.cloud import storage
from google.oauth2 import service_account

from config import config, Config

bootstrap = Bootstrap()
db = SQLAlchemy()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


TaskBase = celery.Task


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

    bootstrap.init_app(app)
    db.init_app(app)
    celery.conf.update(app.config)

    from underground_garage.main import main
    app.register_blueprint(main)

    return app

import underground_garage.models
