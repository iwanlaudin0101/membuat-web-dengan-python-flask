from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator
from app.model.user import User
from app.model.blog import Blog

class RegisterValidate(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken!. Please choose a different one.')

class LoginValidate(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    submit = SubmitField('Login')

class UpdateAccountValidate(FlaskForm):
    name = StringField('Name*', validators=[DataRequired()])
    email = StringField('Email*', validators= [DataRequired(), Email()])
    password = PasswordField('Password*', validators= [Length(min=8)])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg','jpeg','png']),
                        FileSize(max_size=1048576,message='File size is too big')])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken!. Please choose a different one.')
            
class BlogsValidate(FlaskForm):
    slug = StringField('Slug', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Image', validators=[
                        FileAllowed(['jpg','jpeg','png']),
                        FileSize(max_size=1048576, message='File size is too big')])
    submit = SubmitField('Post')

    def validate_slug(self, slug):
        slug = Blog.query.filter_by(slug=slug.data).first()
        if slug:
            raise ValidationError('That slug is taken!. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators= [DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')