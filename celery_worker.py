#!/usr/bin/env python
import os
from underground_garage.app import celery, create_app
from underground_garage import shows

app = create_app(os.getenv('UNDERGROUND_ENV') or 'default')
app.app_context().push()
