from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from pathlib import Path
from tautulli_api import Tautulli

# Get Abs Paths
database = Path('./app/database/database.db').absolute()
template_folder = Path('./app/templates').absolute()
static_folder = Path('./app/static').absolute()

# Create Flask App
app = Flask(__name__, template_folder=template_folder,
            static_folder=static_folder)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ae15187be0a2400ec3028e4f458d4738a585cbf7a9b437be'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=60)

# Database
db = SQLAlchemy(app)

# Bcrypt
bcrypt = Bcrypt(app)

# Login Manager
login_manager = LoginManager(app)

# Tautulli
t = Tautulli()

# Get pms proxy page URL
@app.template_global('get_page')
def get_page(endpoint, *args, **kwargs):
    return t.get_page(endpoint, *args, **kwargs)

from app import routes
