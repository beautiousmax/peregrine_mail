import flask

from views import email_api
from data import database

app = flask.Flask('peregrine')

database.init_database()

app.register_blueprint(email_api.blueprint)
