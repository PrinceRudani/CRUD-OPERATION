import warnings
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize app
app = Flask(__name__)

# Secret key for sessions and cookies
app.secret_key = 'data'

# Database configuration
app.config['SQLALCHEMY_ECHO'] = False  # Set to False in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/FlaskMVCProjectdb'
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# File upload folder
app.config['UPLOAD_FOLDER'] = 'base/static/product_images'

# JWT configuration
jwt = JWTManager(app)

# Initialize DB and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Logger configuration
logging.basicConfig(level=logging.DEBUG)

# App context push
app.app_context().push()

# Import controller module
from base.com import controller
