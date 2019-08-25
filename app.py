import flask
import queue

from views import email_api
from data.database import db

from background_thread import Threading

q = queue.Queue()

app = flask.Flask('peregrine')

app.config['EMAIL_QUEUE'] = q
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///email_db.sqlite'
db.init_app(app)
Threading(q, app)

app.register_blueprint(email_api.blueprint, url_prefix="/api/v1")
