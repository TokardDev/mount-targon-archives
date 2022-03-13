import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .fonctionsDb import *


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def get_matchs(user):
    db = get_db()
    users = AfficherPartiesJoueurs(db.cursor(),user)
    return users

def get_profile(user):
    db = get_db()
    profil = profil_joueur(db.cursor(),user)
    return profil

def get_users():
    db = get_db()
    matches = AfficherListeJoueurs(db.cursor())
    return matches

def init_app(app):
    app.teardown_appcontext(close_db)
