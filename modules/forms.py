from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import StopValidation, InputRequired, Length, EqualTo
from modules.user import usernameExists, load_user


def validateUsernameNotExist(message=None):
    if not message:
        message = "Username already exists"

    def _validate(form, field):
        username = field.data
        if usernameExists(username):
            raise StopValidation(message)

    return _validate


def validateUsernameExist(message=None):
    if not message:
        message = "Username does not exist"

    def _validate(form, field):
        username = field.data
        if not usernameExists(username):
            raise StopValidation(message)

    return _validate


class LoginForm(FlaskForm):
    username = StringField("Username:", [
        InputRequired(message="Please enter a username.")
    ])
    password = PasswordField("Password:", [
        InputRequired(message="Please enter a password.")
    ])

    def validate(self):
        if not super().validate():
            return False

        _username = self.username.data
        _password = self.password.data
        user = load_user(_username)

        if user is None:
            self.username.errors.append("Invalid username")
            return False

        if not user.check_password(_password):
            self.password.errors.append("Wrong password")
            return False

        return True


class LeagueIDForm(FlaskForm):
    leagueID = IntegerField("ESPN League ID:", [
        InputRequired(message="Please enter a league ID.")
    ])


class RegisterForm(FlaskForm):
    username = StringField('Username:', [
        InputRequired(message="Please enter a username."),
        Length(max=40, message="Username must be less than 40 characters."),
        validateUsernameNotExist()
    ])
    password = PasswordField('Password:', [
        InputRequired(message="Please enter a password."),
        EqualTo('confirm', message='Passwords must match.')
    ])
    confirm = PasswordField('Verify Password')
