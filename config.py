import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# Application Instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Flask APP instance
app = connex_app.app

# Sqlite URL 
sqlite_url = "sqlite:///" + os.path.join(basedir, "restaurant.db")

# Setting 
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)