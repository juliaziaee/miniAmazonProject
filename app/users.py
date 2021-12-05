from typing import Type
from flask import render_template, redirect, url_for, flash, request
from flask.app import Flask
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange
from flask_babel import _, lazy_gettext as _l
from datetime import datetime

from .models.user import User
from .models.user import Balance


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))
    street1 = StringField(_l('Street Line 1'), validators=[DataRequired()])
    street2 = StringField(_l('Street Line 2'))
    city = StringField(_l('City'), validators=[DataRequired()])
    state = StringField(_l('State'), validators=[DataRequired()])
    zip = StringField(_l('Postal Code'), validators=[DataRequired(), Length(min=5, max=5)])

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError(_('Already a user with this email.'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.street1.data,
                         form.street2.data,
                         form.city.data,
                         form.state.data,
                         form.zip.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField(_l('Old Password'), validators=[DataRequired()])
    new_password = PasswordField(_l('New Password'), validators=[DataRequired()])
    new_password2 = PasswordField(
        _l('Repeat New Password'), validators=[DataRequired(),
                                           EqualTo('new_password2')])
    submit = SubmitField(_l('Update Password'))

@bp.route("/updatepassword", methods=['GET', 'POST'])
def updatepassword():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        return redirect(url_for('users.accountdetails'))
        # NEED TO ADD FUNCTIONALITY
    return render_template('updatepassword.html', title='Update Password', form=form)


class UpdateUserInfoForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    street1 = StringField(_l('Street Line 1'), validators=[DataRequired()])
    street2 = StringField(_l('Street Line 2'))
    city = StringField(_l('City'), validators=[DataRequired()])
    state = StringField(_l('State'), validators=[DataRequired()])
    zip = StringField(_l('Postal Code'), validators=[DataRequired(), Length(min=5, max=5)])
    submit = SubmitField(_l('Update'))

    # def validate_email(self, email):
    #     if User.email_exists(email.data):
    #         raise ValidationError(_('Already a user with this email.'))

@bp.route('/updateuserinfo', methods=['GET', 'POST'])
def updateuserinfo():
    form = UpdateUserInfoForm()
    if form.validate_on_submit():
        if User.update(current_user.id,
                         form.email.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.street1.data,
                         form.street2.data,
                         form.city.data,
                         form.state.data,
                         form.zip.data):
            return redirect(url_for('users.accountdetails'))
    return render_template('updateuserinfo.html', title='Update Information', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


@bp.route("/accountdetails")
def accountdetails():
    return render_template("accountdetails.html", title="Home page")

@bp.route("/orderhistory")
def orderhistory():
    return render_template("orderhistory.html", title="Home page")

class Funds(FlaskForm):
    amount = DecimalField(_l('Amount'))
    submit = SubmitField(_l('Submit'))
    
    def validate_amount(form, field):
        if "." in (str(field.data)):
            x = (str(field.data)).split(".")[1]
            if len(x)>2:
                raise ValidationError("Cannot exceed two decimal places")

@bp.route("/accountbalance", methods=['GET', 'POST'])
def accountbalance():
    error = None
    if current_user.is_authenticated:
        userbal = Balance.getBalance(current_user.id)
        form = Funds()
        if form.validate_on_submit():
            if Balance.updateBalance(current_user.id, datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'), form.amount.data) == current_user.id:
                return redirect(url_for('users.accountbalance'))
            else:
                error = (Balance.updateBalance(current_user.id, datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'), form.amount.data).split("CONTEXT"))[0]
        return render_template("accountbalance.html", title="Account Balance", balance=userbal, form=form, error = error)
    else: return render_template("accountbalance.html", title="Account Balance")
    
@bp.route("/userdetails", methods=['GET', 'POST'])
def userdetails():
    uid = request.args.get('uid', None)
    user = User.get(uid)
    return render_template('userdetails.html', user=user)

