from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.secret_key = 'bardzo_tajny_klucz'  # Ustaw tajny klucz tutaj
# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import routes
