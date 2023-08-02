from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '6e9142134c8c3b306eef0ce3c1d5d585'

if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../comunidade.db"


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

database = SQLAlchemy(app)

from comunidadeintergard import routes


def create_database_if_not_exists():
    engine = sqlalchemy.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sqlalchemy.inspect(engine)
    if not inspector.has_table('usuario'):
        with app.app_context():
            database.create_all()
            print("Base de dados criada com sucesso!")
    else:
        print("Base de dados já existe!")

create_database_if_not_exists()


