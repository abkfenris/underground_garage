"""
Show model
"""
from underground_garage.app import db


class Show(db.Model):
    """
    Show model

    Arguments:
        id (int): Primary Show id
        episode (int): Show number
        name (str): Show name
        dt (datetime): Show date
        description (text): Description of the show
        url (str): Url of the show page
        file (str): filename of show
    """
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    episode = db.Column(db.Integer)
    name = db.Column(db.String(160))
    dt = db.Column(db.DateTime)
    description = db.Column(db.Text)
    url = db.Column(db.String(320))
    file = db.Column(db.String(320))

    def __repr__(self):
        if self.episode and self.name:
            return '<Show {episode} - {name}>'.format(episode=self.episode,
                                                      name=self.name)
        return  '<Show {url}>'.format(url=self.url)
