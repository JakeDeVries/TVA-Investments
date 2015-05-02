from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jefferson1776@localhost/credentials'
 
from app import views
from .models import db
db.init_app(app)