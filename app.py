from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://league_analyzer:a988Jqye%Lgkw^t5@localhost:3306/ladata"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.secret_key = "dfgsdfgwerv@^&#nmkvaw,3"

import views

if __name__ == '__main__':
    app.run()

