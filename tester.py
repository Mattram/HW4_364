import os
import requests
import json
from giphy_api_key import api_key
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash

# Imports for login management
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://postgres:password@localhost/mattramHW4db" #TODOdone 364: You should edit this to correspond to the database name YOURUNIQNAMEHW4db and create the database of that name (with whatever your uniqname is; for example, my database would be jczettaHW4db). You may also need to edit the database URL further if your computer requires a password for you to run this.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# App addition setups
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) # set up login manager

def get_gifs_from_giphy(search_string):
    """ Returns data from Giphy API with up to 5 gifs corresponding to the search input"""
    baseurl = "https://api.giphy.com/v1/gifs/search"
    params = {}
    params["api_key"] = api_key
    params["q"] = search_string
    params["limit"] = 5
    o = requests.get(baseurl, params = params)
    d = json.loads(o.text)
    print(type(d))
    print(d.keys())
    gifs = d['data']
    print(type(gifs))
    return gifs

@app.route('/', methods=['GET', 'POST'])
def index():
    d = get_gifs_from_giphy("stop")
    print(d.title())

    return "look at your terminal"
    # TODO 364: Edit this view function, which has a provided return statement, so that the GifSearchForm can be rendered.
    # If the form is submitted successfully:
    # invoke get_or_create_search_term on the form input and redirect to the function corresponding to the path /gifs_searched/<search_term> in order to see the results of the gif search. (Just a couple lines of code!)

    # HINT: invoking url_for with a named argument will send additional data. e.g. url_for('artist_info',artist='solange') would send the data 'solange' to a route /artist_info/<artist>
    return render_template('index.html',form=form)

if __name__ == '__main__':
    db.create_all()
    manager.run()
