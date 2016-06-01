# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from celery import Celery
from flask import Flask  # , render_template
from flask_bootstrap import Bootstrap
# from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_cloudy import Storage

from config import config, Config

bootstrap = Bootstrap()
db = SQLAlchemy()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
storage = Storage()


def create_app(config_name):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    '''
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)
    storage.init_app(app)
    celery.conf.update(app.config)

    from underground_garage.main import main
    app.register_blueprint(main)

    return app

import underground_garage.models
