# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template

from config import config


def create_app(config_name):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    '''
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    return app
