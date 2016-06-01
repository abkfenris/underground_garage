import os
import logging

from underground_garage.app import create_app

env = os.environ.get('UNDERGROUND_CONFIG')

app = create_app(env)


@app.before_first_request
def setup_logging():
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

if __name__ == '__main__':
    app.run()
