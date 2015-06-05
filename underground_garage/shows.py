"""
Utilities to get shows, and individual media files
"""
from collections import namedtuple
import time

import arrow
from bs4 import BeautifulSoup
from flask import current_app
from pydub import AudioSegment
import requests

from underground_garage.app import celery
from underground_garage.app import db
from underground_garage.models import Show


URL_STUB = 'http://undergroundgarage.com'


def archivepages():
    """
    From the Underground Garage index page (as of 2015-06-02) return a list
    of archived show page urls
    """
    show_list = []
    index_r = requests.get(URL_STUB)
    index_soup = BeautifulSoup(index_r.text, 'html.parser')
    for span in index_soup.findAll('span'):
        try:
            if 'Archived Shows' in span.contents[0]:
                archive_span = span
                break
        except IndexError:
            pass
    next_span = archive_span
    while True:
        try:
            next_span = next_span.next
        except AttributeError:
            break
        try:
            if next_span.name == 'a':
                if 'shows-' in next_span.attrs['href'] or 'Shows-' in next_span.attrs['href']:
                    if '.html' not in next_span.attrs['href']:
                        show_list.append(URL_STUB + next_span.attrs['href'])
        except AttributeError:
            pass
        except KeyError:
            pass
    return show_list


def showlinks(archive_url):
    """
    Takes the url for an archive page and returns a list of urls to shows
    """
    r = requests.get(archive_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links_to_shows = []
    for h4 in soup.findAll('h4'):
        if 'Shows' in str(h4.contents[0]):
            archive_header = h4
            break
    span = archive_header.findNext('span')
    next_span = span
    while True:
        try:
            next_span = next_span.next
        except AttributeError:
            break
        try:
            if next_span.name == 'a':
                if 'Shows' in next_span.attrs['href'] or 'shows' in next_span.attrs['href']:
                    url = URL_STUB + next_span.attrs['href']
                    if url not in links_to_shows:
                        links_to_shows.append(url)
        except AttributeError:
            pass
    return links_to_shows


def showsinarchive():
    """
    Returns a list of urls for all shows in the archive
    """
    links = []
    for archive_url in archivepages():
        links = links + showlinks(archive_url)
    return links


def showplayerlink(show_url):
    """
    Takes the full url to a show, and returns a url to the player for the show
    """
    r = requests.get(show_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for href in soup.findAll('a'):
        if 'onclick' in href.attrs:
            if '/jw/playlist.php?id=' in href.attrs['onclick']:
                elements = str(href).split('\'')
                for part in elements:
                    if '/jw/playlist.php?id=' in part:
                        return URL_STUB + part


def playlistparts(playlist_part):
    """
    Takes the correct part of a playlist
    and returns a list of urls to show segments
    """
    output = []
    text = playlist_part.replace(':', ',').split(',')
    for part in text:
        if '.mp3' in part:
            output.append('http://undergroundgarage.com' + part.strip('"'))
    return output


def showplaylist(show_url):
    """
    Takes the full url to a show
    and returns a list with the urls to show segments
    """
    r = requests.get(showplayerlink(show_url))
    soup = BeautifulSoup(r.text, 'html.parser')
    for script in soup.findAll('script'):
        try:
            if 'playlist' in script.contents[0]:
                text = str(script).replace(']', '[').split('[')
                for part in text:
                    if 'file' in part:
                        return playlistparts(part)
        except IndexError:
            pass


def showinfo(show_url):
    """
    Returns a NamedTuple containing the info from show_url
    """
    showinfo = namedtuple('ShowInfo', 'number title date description')
    r = requests.get(show_url)
    if r.status_code != 200:
        while True:
            time.sleep(10)
            r = requests.get(show_url)
            if r.status_code == 200:
                break
    soup = BeautifulSoup(r.text, 'html.parser')
    number = int(soup.title.contents[0].split('-')[0].strip().split(' ')[1].strip(':'))
    title = soup.title.contents[0].split('-')[1].strip()
    dt =  arrow.get(soup.find_all('div', class_='pos-description')[0].div.contents[2],
                    'dddd, D MMMM YYYY').datetime
    desc = soup.find_all('div', class_='pos-description')[0].div.next_sibling.contents[1].get_text()
    return showinfo(number=number, title=title, date=dt, description=desc)


@celery.task
def combinelist(playlist, id=None, filename='list.mp3'):
    """
    Combines a list of mp3 urls into a single file
    """
    sound = AudioSegment.silent(duration=0)
    print('Retrieving playlist {playlist} for file {filename}'.format(
                playlist=playlist,
                filename=filename))
    total = len(playlist)
    for counter, url in enumerate(playlist):
        print('Retriveing part {counter} of {total}'.format(
                    counter=counter + 1,
                    total=total))
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            while True:
                print r.status_code
                time.sleep(10)
                r = requests.get(url, stream=True)
                if r.status_code == 200:
                    break
        r.raw.decode_content = True
        sound = sound + AudioSegment.from_mp3(r.raw)
    sound.export(filename, format='mp3')
    print('Completed file: {filename}'.format(filename=filename))
    if id is not None:
        s = Show.query.filter_by(id=id).first()
        print s
        s.file = filename
        db.session.add(s)
        db.session.commit()


@celery.task
def updateshows():
    """
    Get the current list of shows in the archive,
    then add the urls to the database
    """
    with current_app.app_context():
        print('Updating shows')
        showlist = showsinarchive()
        print('Found {num} shows'.format(num=len(showlist)))
        for show in showlist:
            s = Show.query.filter_by(url=show).first()
            if s is None:
                s = Show(url=show)
                db.session.add(s)
        print('Adding shows:')
        for obj in db.session:
            print obj
        db.session.commit()
    without = showswithout()
    print without
    for show in without:
        updateshowdetails.delay(show.url)


@celery.task
def updateshowdetails(url):
    """
    Update the details of a show by url
    """
    print('Updating details for {url}'.format(url=url))
    info = showinfo(url)
    s = Show.query.filter_by(url=url).first()
    s.name = info.title
    s.episode = info.number
    s.dt = info.date
    s.description = info.description
    db.session.add(s)
    db.session.commit()
    time.sleep(1)


def showswithout():
    """
    Return a list of urls for shows without an episode
    """
    return Show.query.filter_by(episode=None).all()
