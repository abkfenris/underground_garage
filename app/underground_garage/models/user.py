"""
Models for Users and Roles
"""
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore

from underground_garage.app import db


roles_users = db.Table('roles_users',
                       db.Column('user_id',
                                 db.Integer(),
                                 db.ForeignKey('users.id')),
                       db.Column('role_id',
                                 db.Integer(),
                                 db.ForeignKey('roles.id')))


class Role(db.Model, RoleMixin):
    """
    Role Model

    Using Flask-Security's RoleMixin

    Arguments:
        id (int): Primary Role Key
        name (str): Role name for reference in admin and for restrictions
        description (str): Role Description
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        if self.description is not None:
            return '{name} - {desc}'.format(name=self.name, desc=self.description)
        return '{name}'.format(name=self.name)


class User(db.Model, UserMixin):
    """
    User Model

    Arguments:
        id (int): Primary User Key
        username (str): Unique username as chosen by the user
        email (str): User's email address
        password (str): User's hashed password
        active (bool): Is the user activated
        confirmed_at (datetime): When the user was confirmed
        roles (list): List of role objects that the user has
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {name}'.format(name=self.username)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
