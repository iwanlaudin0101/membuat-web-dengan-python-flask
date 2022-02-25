import os
import secrets
from flask import current_app, url_for
from app import db, bcrypt, login_manager, mail
from app.model.user import User
from app.form_validate import BlogsValidate
from flask_mail import Message

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def hashed_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password_hash(pw_hash, password):
    return bcrypt.check_password_hash(pw_hash, password)

def save_picture(form_picture, path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, path, picture_fn)
    form_picture.save(picture_path)

    return picture_fn

def delete_file(filename, path):
    picture_path = os.path.join(current_app.root_path, path, filename)    
    os.remove(picture_path)

def sen_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=['user.email'])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)