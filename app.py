import flask

from views import email_api
from data.database import db

app = flask.Flask('peregrine')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///email_db.sqlite'

db.init_app(app)

app.register_blueprint(email_api.blueprint, url_prefix="/api/v1")
