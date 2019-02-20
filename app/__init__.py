from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key =  b'_5#y2L"F4Q8z\n\xec]/'

db = SQLAlchemy(app)
from app import routes

