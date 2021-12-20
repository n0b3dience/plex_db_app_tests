from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.fields.simple import EmailField, PasswordField
from wtforms.validators import (
    DataRequired, 
    Email, 
    EqualTo, 
    Length, 
    ValidationError)
from app.models import User


class UserSignupForm(FlaskForm):
    # Username
    username = StringField('User Name', 
        validators=[DataRequired(), Length(min=4, max=80)])
    # Email
    email = EmailField('Email', 
        validators=[DataRequired(), Length(max=120), 
            Email(message=('Not a valid email address.'))])
    # Password
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=4, max=120)])
    # Password Confirmation
    confirm_password = PasswordField(
        'Password', validators=[DataRequired(), 
            EqualTo('password', message='Passwords do not match!')])
    # Submit
    submit = SubmitField('Submit')

    def validate_user(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'This username is already taken. Please, choose another.')
    
    def validate_email(self, email):
        email = User.query.filter_by(username=email.data).first()
        if email:
            raise ValidationError(
                'This email address has already been registered.')


class LoginForm(FlaskForm):
    # Email
    email = EmailField('Email', 
        validators=[DataRequired(), Length(max=120), 
            Email(message=('Not a valid email address.'))])
    # Password
    password = PasswordField(
        'Password', [DataRequired(), Length(min=4, max=120)])
    # Remember
    remember = BooleanField('Remember Me')
    # Submit
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    # Title
    title = StringField("Post Title", 
        validators=[DataRequired(), Length(max=255, 
            message='Your title cannot exceed 255 characters')])
    # Content
    content = StringField("Post Content", 
        validators=[DataRequired(), Length(max=2000, 
            message='Your post is too long (max 2000 characters)')])
    # Submit
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    # Content
    content = StringField("Comment", 
        validators=[DataRequired(), Length(max=2000, 
            message='Your message is too long (max 2000 characters)')])
    # Submit
    submit = SubmitField("Submit")


class ReplyForm(FlaskForm):
    # Content
    content = StringField("Reply", 
        validators=[DataRequired(), Length(max=2000, 
            message='Your message is too long (max 2000 characters)')])
    # Submit
    submit = SubmitField("Submit")


class Reply2Form(FlaskForm):
    # Content
    content = StringField("Reply", 
        validators=[DataRequired(), Length(max=2000, 
            message='Your message is too long (max 2000 characters)')])
    # Submit
    submit = SubmitField("Submit")
    