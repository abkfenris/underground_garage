"""
The main public routes to view the site
"""
import os
import logging
from datetime import timedelta

from flask import render_template, redirect, url_for, abort, send_from_directory, current_app

from underground_garage import shows
from underground_garage.app import storage_client_bucket
from underground_garage.models import Show
from config import basedir

from . import main

logger = logging.getLogger(__name__)

@main.route('/')
def index():
    """**/**

    Index page with list of shows
    """
    return render_template('index.html', Show=Show)


@main.route('/feed/')
def feed():
    """**/feed/**

    Podcast feed
    """
    #shows.updateshows.delay()
    return render_template('feed.rss',
                           Show=Show,
                           last_show_date=Show.query.order_by(
                                Show.episode.desc()).filter(
                                    Show.episode != None).first().dt)


@main.route('/about/')
def about():
    """**/about/**

    About this site
    """
    return render_template('about.html')


@main.route('/update/')
def update():
    """**/update/**

    Update listing of shows
    """
    return redirect(url_for('.index'))


@main.route('/show/<episode>.mp3')
def mp3(episode):
    """**/show/<id>.mp3**

    If file is avaliable, then serve it, otherwise get file and then serve it
    """
    s = Show.query.filter_by(episode=episode).first_or_404()
    filename = '{episode}.mp3'.format(episode=s.episode)

    client, bucket = storage_client_bucket(current_app)

    mp3 = bucket.get_blob(filename)

    try:
        download_url = mp3.generate_signed_url(timedelta(seconds=18000))
        return redirect(download_url)
    except AttributeError:
        current_app.logger.warning('Unable to load episode {episode}'.format(episode=episode))
        shows.combinelist.delay(show_id=s.id, filename=filename)
        #current_app.logger.warning('{pl} - {id} - {filename}'.format(pl=', '.join(pl), id=s.id, filename=filename))

        abort(404)
        #return render_template('404.html'), 404
