from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self) -> str:
        s = Serializer(current_app.config['SECRET_KEY'])
        token = s.dumps({'user_id': self.id})# Dla celów debugowania
        return token

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)