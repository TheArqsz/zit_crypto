from flask import Flask
from .config import BaseConfig
import os 

app = Flask('CryptHelper')
app.config.from_object(BaseConfig)
from logged_out.routes import logged_out_bp
from logged_in.routes import logged_in_bp
from reroute.routes import rerouting_bp
app.register_blueprint(logged_out_bp, url_prefix="/out")
app.register_blueprint(logged_in_bp, url_prefix="/in")
app.register_blueprint(rerouting_bp)
from database.models import db
db.init_app(app)
with app.app_context():
    db.create_all()