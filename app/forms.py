from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField
from wtforms import ValidationError


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            validators.input_required(),
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            validators.input_required(),
        ]
    )
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            validators.input_required(),
        ])
    email = StringField(
        'Email',
        validators=[
            validators.input_required(),
            validators.email(),
        ])
    password = PasswordField(
        'Password',
        validators=[
            validators.input_required(),
            validators.length(min=8, max=30)
        ])
    password2 = PasswordField(
        'Repeat Password',
        validators=[
            validators.input_required(),
            validators.equal_to('password'),
        ])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already in use.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already in use.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            validators.input_required(),
            validators.email(),
        ])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[validators.input_required()])
    password2 = PasswordField(
        'Repeat Password',
        validators=[
            validators.input_required(),
            validators.equal_to('password'),
        ])
    submit = SubmitField('Request Password Reset')
