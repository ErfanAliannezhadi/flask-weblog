from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models import UserModel
from flask_login import current_user


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    def validate_username(self, username):
        user = UserModel.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username already exists')

    def validate_email(self, email):
        user = UserModel.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email already exists')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    def validate_username(self, username):
        if current_user.username != username.data:
            user = UserModel.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username already exists')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = UserModel.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The email already exists')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
