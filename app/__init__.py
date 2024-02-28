from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.secret_key = 'bardzo_tajny_klucz'  # Ustaw tajny klucz tutaj
# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# obsługa maili
from flask_mail import Mail

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'systemy.rozproszone2024@gmail.com'
app.config['MAIL_PASSWORD'] = 'ebcm ueni tkeb ecmu'
app.config['MAIL_DEFAULT_SENDER'] = 'systemy.rozproszone2024@gmail.com'

mail = Mail(app)


from app import routes
