"""
Utilities to get shows, and individual media files
"""
import requests
from bs4 import BeautifulSoup


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
                    links_to_shows.append(URL_STUB + next_span.attrs['href'])
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
