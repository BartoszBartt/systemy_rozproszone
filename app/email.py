from flask_mail import Message
from app import mail
from flask import url_for

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Resetowanie hasła',
                  recipients=[user.email])
    link = url_for('reset_token', token=token, _external=True)
    msg.body = f'''Aby zresetować hasło, odwiedź poniższy link:
{link}

Jeśli to nie Ty żądałeś resetowania hasła, zignoruj tę wiadomość.
'''
    mail.send(msg)
