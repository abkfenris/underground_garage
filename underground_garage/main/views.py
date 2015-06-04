"""
The main public routes to view the site
"""

from flask import render_template, redirect, url_for

from underground_garage import shows
from underground_garage.models import Show

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
