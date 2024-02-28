from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import User

from flask_mail import Message
from app import mail, app
from flask import url_for
from app.email import send_reset_email

users = {}


# wygląd strony głównej
@app.route('/')
def index():
    return redirect(url_for('login'))

# logowanie
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']  # Pobierz email z formularza

        # Sprawdź, czy nazwa użytkownika lub email już istnieje
        user_by_username = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()

        if user_by_username:
            flash('Nazwa użytkownika jest już zajęta.')
            return redirect(url_for('signup'))
        if user_by_email:
            flash('Adres email jest już używany.')
            return redirect(url_for('signup'))
        
        # Jeśli wszystko jest w porządku, tworzymy nowego użytkownika
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Rejestracja zakończona sukcesem.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Nieprawidłowa nazwa użytkownika lub hasło.')
            return redirect(url_for('login'))
        # Logika sesji/logowania użytkownika
        flash('Zalogowano pomyślnie.')
        return redirect(url_for('menu'))
    return render_template('login.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            send_reset_email(user)
            flash('Instrukcje resetowania hasła zostały wysłane na Twój adres email.', 'info')
        else:
            flash('Nie ma konta z tym adresem email.', 'warning')
        return redirect(url_for('login'))
    return render_template('reset_request.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('To jest nieprawidłowy lub wygasły token', 'warning')
        return redirect(url_for('reset_request'))
    if request.method == 'POST':
        password = request.form['password']
        user.set_password(password)
        db.session.commit()
        flash('Twoje hasło zostało zaktualizowane!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html')

# @app.route('/reset_password')
# def reset_password():
#     # Tutaj logika dla resetowania hasła
#     return render_template('reset_password.html')


@app.route('/menu')
def menu():
    # Tutaj wyświetlamy menu po pomyślnym zalogowaniu
    return render_template('menu.html')

