from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

users = {}

@app.route('/')
def index():
    return '<h1>Strona Główna</h1><a href="/login">Logowanie</a> | <a href="/signup">Rejestracja</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        
        if user and check_password_hash(user['password'], password):
            print(f'Pomyślne logowanie: {username}')
            return f'Zalogowano jako {username}'
        else:
            print(f'Błędne dane logowania dla: {username}')
            return 'Błędne dane logowania'

    return '''
        <form method="post">
            Nazwa użytkownika: <input type="text" name="username"><br>
            Hasło: <input type="password" name="password"><br>
            <input type="submit" value="Zaloguj się">
        </form>
    '''

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        if username in users:
            return 'Użytkownik już istnieje'
        
        users[username] = {'email': email, 'password': hashed_password}
        print(f'Rejestracja: {username}, Email: {email}, Hasło: {hashed_password}')
        return f'Rejestrujesz się jako {username} z emailem {email}'
    
    return '''
        <form method="post">
            Nazwa użytkownika: <input type="text" name="username"><br>
            Email: <input type="email" name="email"><br>
            Hasło: <input type="password" name="password"><br>
            <input type="submit" value="Zarejestruj się">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
