import warnings
from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)


app.secret_key = 'data'

app.config['SQLALCHEMY_ECHO'] = True

app.config['UPLOAD_FOLDER'] = 'base/static/product_images'

app.config['PERMENANT_SESSION_LIFETIME'] = timedelta(minutes=30)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/FlaskMVCProjectdb'

app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

app.config['JWT_SECRET_KEY'] = 'data'

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)

app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

jwt = JWTManager(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

app.app_context().push()

from base.com import controller
