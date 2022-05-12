from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
from json_models import JsonCdLibrary

import os
from dotenv import load_dotenv
from config import Config
from flask_migrate import Migrate


app = Flask(__name__)

app.config.from_object(Config())

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import models, routes