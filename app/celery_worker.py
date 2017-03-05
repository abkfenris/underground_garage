#!/usr/bin/env python
import os
from underground_garage.app import celery, create_app
from underground_garage import shows

celery.conf.beat_schedule = {
    'update-1-hour': {
        'task': 'underground_garage.shows.updateshows',
        'schedule': crontab(hour='*/1')
    }
}

app = create_app(os.getenv('UNDERGROUND_ENV') or 'default')
app.app_context().push()
