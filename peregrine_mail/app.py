import queue
import json
from pathlib import Path
import os

import flask

from peregrine_mail.views import email_api
from peregrine_mail.data.database import db
from peregrine_mail.background_thread import Threading

project_root = os.path.abspath(os.path.dirname(__file__))


app = flask.Flask('peregrine')

# Background thread requirements
email_queue = queue.Queue()
app.config['EMAIL_QUEUE'] = email_queue

# Add config file data to app config
config_file = Path(project_root, os.pardir, "config.json")
if not config_file.exists():
    raise Exception(f"No config file found! Expected it at {config_file.absolute()}")
data = json.loads(config_file.read_text())

app.config['SMTP'] = data['smtp']

# Database setup
sqlite_db_file = Path(project_root, os.pardir, "email_db.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{sqlite_db_file}'

db.init_app(app)
with app.app_context():
    db.create_all()

# Start the background thread

Threading(email_queue, app)

app.register_blueprint(email_api.blueprint, url_prefix="/api/v1")
