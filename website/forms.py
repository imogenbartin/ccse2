from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired


class RegisterForm(FlaskForm):

    #Creating a register form, validators are there to ensure fields are written in before submitting, length is there for security
    email=EmailField('Email', validators=[DataRequired(), length(min=2)])
    username = StringField('Username', validators=[DataRequired(), length(min=6)])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8)])
    confirmPassword = PasswordField('Confirm password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class PasswordChangeForm(FlaskForm):
    currentPassword = PasswordField('Current Password', validators=[DataRequired(), length(min=6)]) #user must enter their current pass before changing it
    newPassword = PasswordField('New password', validators=[DataRequired(), length(min=6)])
    confirmNewPass = PasswordField('Confirm new password', validators=[DataRequired(), length(min=6)])
    changePassword = SubmitField('Change Password')

class ShopItemsForm(FlaskForm):
    productName = StringField('Name of Product', validators=[DataRequired()])
    price = FloatField('Current Price', validators=[DataRequired()])
    itemAmount = IntegerField('In stock', validators=[DataRequired(), NumberRange(min=0)]) #making sure the amount in stock cannot be >0
    productPicture = FileField('Product Picture', validators=[FileRequired()]) 

    addProduct = SubmitField('Add Product')
    updateProduct = SubmitField('Update')