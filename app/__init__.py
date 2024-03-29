from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_apscheduler import APScheduler
import os

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
with app.app_context():
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == "true":
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()



from app import routes, models

with app.app_context():
    db.create_all()
