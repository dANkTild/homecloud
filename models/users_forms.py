from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.fields import PasswordField, StringField
from wtforms.validators import DataRequired


# TODO: Приделать нормальные валидаторы и сообщения об ошибках
class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    passwd = PasswordField("Пароль", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    passwd = PasswordField("Пароль", validators=[DataRequired()])
    repasswd = PasswordField("Повторите пароль", validators=[DataRequired()])
