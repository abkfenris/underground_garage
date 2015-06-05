"""
The main public routes to view the site
"""
import os

from flask import render_template, redirect, url_for, abort, send_from_directory

from underground_garage import shows
from underground_garage.models import Show
from config import basedir

from . import main


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
    return render_template('feed.rss', Show=Show)


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
    shows.updateshows.delay()
    return redirect(url_for('.index'))


@main.route('/show/<episode>.mp3')
def mp3(episode):
    """**/show/<id>.mp3**

    If file is avaliable, then serve it, otherwise get file and then serve it
    """
    s = Show.query.filter_by(episode=episode).first_or_404()
    if s.file is None:
        pl = shows.showplaylist(s.url)
        filename = 'underground_garage/static/shows/{episode}.mp3'.format(episode=s.episode)
        shows.combinelist.delay(pl, id=s.id, filename=filename)
        abort(404)
    else:
        path, file = os.path.split(s.file)
        path = os.path.join(basedir, path)
        return send_from_directory(path, file)
