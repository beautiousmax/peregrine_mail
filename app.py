import queue
import json
from pathlib import Path

import flask

from views import email_api
from data.database import db
from background_thread import Threading

q = queue.Queue()

app = flask.Flask('peregrine')

app.config['EMAIL_QUEUE'] = q
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///email_db.sqlite'

config_file = Path("config.json")
if not config_file.exists():
    raise Exception(f"No config file found! Expected it at {config_file.absolute()}")
data = json.loads(config_file.read_text())

app.config['SMTP'] = data['smtp']

db.init_app(app)
with app.app_context():
    db.create_all()

Threading(q, app)

app.register_blueprint(email_api.blueprint, url_prefix="/api/v1")
