#!/usr/bin/env python
import os

from celery.task.schedules import crontab
from raven import Client
from raven.contrib.celery import register_signal, register_logger_signal

from underground_garage.app import celery, create_app, logging_map
from underground_garage import shows

celery.conf.beat_schedule = {
    'update-1-hour': {
        'task': 'underground_garage.shows.updateshows',
        'schedule': crontab(minute=0)
    }
}

app = create_app(os.getenv('UNDERGROUND_CONFIG') or 'default')
app.app_context().push()

client = Client(os.environ.get('SENTRY_DSN'))

register_logger_signal(client, logging_map[os.environ.get('LOG_LEVEL', 'INFO')])
register_signal(client)