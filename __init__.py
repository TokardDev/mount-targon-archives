import os

from flask import Flask
from . import db
from markupsafe import escape
from flask import Flask, render_template,redirect


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'leagueOfLegends.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello

    @app.route('/')
    def defaultUrl():
        return redirect("/users")

    @app.route('/users/')
    def users():
        users = db.get_users()
        return render_template('index.html',profils=users)
    
    @app.route('/tuto/')
    def tuto():
        return render_template('tuto.html')
    
    @app.route('/users/<user>')
    def user(user):
        parties = db.get_matchs(str(user))
        profile = db.get_profile(str(user))
        print(profile)
        return render_template('profil.html',matches=parties,profile=profile,user=user)


    db.init_app(app)


    return app


    
