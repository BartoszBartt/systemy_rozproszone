from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import User
users = {}


# wygląd strony głównej
@app.route('/')
def index():
    return redirect(url_for('login'))


# Przykładowe dane użytkownika dla celów demonstracyjnych
users = {"user1": "password1"}

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


# resetowanie hasła
@app.route('/reset_password')
def reset_password():
    # Tutaj logika dla resetowania hasła
    return render_template('reset_password.html')

@app.route('/menu')
def menu():
    # Tutaj wyświetlamy menu po pomyślnym zalogowaniu
    return render_template('menu.html')
