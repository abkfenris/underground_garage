underground_garage
==================

Flask app to turn the Underground Garage Archive into a podcast

.. image:: https://img.shields.io/travis/abkfenris/underground_garage.svg
    :target: https://travis-ci.org/abkfenris/underground_garage
.. image:: https://img.shields.io/coveralls/abkfenris/underground_garage.svg
    :target: https://coveralls.io/r/abkfenris/underground_garage
.. image:: https://img.shields.io/github/issues/abkfenris/underground_garage.svg
    :target: https://github.com/abkfenris/underground_garage/issues
.. image:: https://landscape.io/github/abkfenris/underground_garage/master/landscape.svg?style=flat
   :target: https://landscape.io/github/abkfenris/underground_garage/master
   :alt: Code Health
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/abkfenris/underground_garage

underground_garage is a web app that takes the archived Little Steven's
Underground Garage, creates a single file per show, and makes them avalaible as
a podcast.

The homepage gives a listing of shows, if the file has been created or not, and
lets you download the file if it is, or ask the app to create the file.

To fire it up, start by running `pip install -r requirements/prod.txt`.
Start up postgresql and create a database called underground_garage.
Then 'redis-server' in one terminal,
'celery worker -A celery_worker.celery --loglevel=info' in another,
and finally `python manage.py runserver` in a third.

Navigate to 127.0.0.1:631:5000 (or whatever the manage.py terminal tells you),
and hit update, and it will start getting information about shows and updating
details.
