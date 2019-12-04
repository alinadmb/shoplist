from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, List, Item

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ListCreationForm(FlaskForm):
    listname = StringField('Новый список', validators=[DataRequired()])
    submit = SubmitField('Создать')

class ListEditionForm(FlaskForm):
    listname = StringField('Новое название', validators=[DataRequired()])
    submit = SubmitField('Изменить')

class ItemAdditionForm(FlaskForm):
    itemname = StringField('Новый продукт', validators=[DataRequired()])
    submit = SubmitField('Добавить')

class DeleteListForm(FlaskForm):
    delete = SubmitField('Удалить список')

class DeleteItemForm(FlaskForm, item_id):
    item = Item.query.filter_by(id=item_id)
    delete = SubmitField('Удалить продукт')