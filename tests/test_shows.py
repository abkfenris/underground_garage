from underground_garage import shows


def test_playlist():
    playlist = shows.showplaylist(shows.showsinarchive()[0])
    for url in playlist:
        assert '.mp3' in url
