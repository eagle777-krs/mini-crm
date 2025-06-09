from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, TextAreaField, DateField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Optional
from datetime import date
from app.models import DealType

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Зарегистрироваться')

class UserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Создать пользователя')

class ClientForm(FlaskForm):
    name = StringField('Имя клиента', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Телефон', validators=[Optional(), Length(max=12)])
    submit = SubmitField('Сохранить')

class DealForm(FlaskForm):
    client_id = SelectField('Клиент', coerce=int, validators=[DataRequired()])
    amount = DecimalField('Сумма сделки', places=2, validators=[DataRequired()])
    status = SelectField('Статус сделки', choices=[(choice.value, choice.name) for choice in DealType],
    validators=[DataRequired()]
)
    description = TextAreaField('Описание', validators=[Optional(), Length(max=255)])
    date_start = DateField('Дата начала', default=date.today, validators=[DataRequired()])
    date_close = DateField('Дата закрытия', validators=[Optional()])
    submit = SubmitField('Сохранить сделку')