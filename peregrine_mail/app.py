import json
import logging
import queue
import os
from pathlib import Path
import sys

import flask

from peregrine_mail.views import email_api
from peregrine_mail.data.database import db
from peregrine_mail.background_thread import Threading

project_root = os.path.abspath(os.path.dirname(__file__))


app = flask.Flask('peregrine')

# Logging
logger = logging.getLogger('peregrine')
stream = logging.StreamHandler(stream=sys.stdout)
stream.setFormatter(logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s'))
logger.addHandler(stream)

# Background thread requirements
email_queue = queue.Queue()
app.config['EMAIL_QUEUE'] = email_queue

# Add config file data to app config
config_file = Path(project_root, os.pardir, 'config.json')
if not config_file.exists():
    raise Exception(f'No config file found! Expected it at {config_file.resolve()}')
data = json.loads(config_file.read_text())

app.config['SMTP'] = data['smtp_server']
app.config['PEREGRINE_MAIL'] = data['peregrine_mail']

log_level = logging.getLevelName(data['peregrine_mail']['log_level'].upper())
if log_level not in (0, 10, 20, 30, 40, 50):
    print("Log level was indeterminable, setting to DEBUG (choices are DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    log_level = 10
stream.setLevel(log_level)
logger.setLevel(log_level)

# Database setup
sqlite_db_file = Path(project_root, os.pardir, 'email_db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{sqlite_db_file}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# Start the background thread

Threading(email_queue, app)

app.register_blueprint(email_api.blueprint, url_prefix='/api/v1')


@app.route('/')
def homepage():
    return 'Welcome to Peregrine Mail!'

