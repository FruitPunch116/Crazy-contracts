#!/usr/bin/env python3

from models import db, User, Contractor

from flask import Flask, jsonify, request, session
# from flask_cors import CORS
from flask_migrate import Migrate
# from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = b'm~\xb6E6\x8b\xe9\xf0\x9d\xa7\x81\x8b\x91&aC\xc1\x7f\xe1\x11\xecn\xeeW\xa1\xf6vT\x96\xb9N\x0b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate (app, db)

db.init_app(app)

if __name__ == ("__main__"):
    app.run (port=8001, debug=True)