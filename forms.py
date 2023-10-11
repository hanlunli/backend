from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
import sqlite3

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_username(self, username):
        conn = sqlite3.connect('login.db')
        curs = conn.cursor()
        curs.execute("SELECT username FROM login WHERE username = ?", (username.data,))
        valusername = curs.fetchone()
        conn.close()  # Close the database connection

        if valusername is None:
            raise ValidationError('This username is not registered. Please register before login')
