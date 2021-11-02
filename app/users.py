from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_babel import _, lazy_gettext as _l

from .models.user import User


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

class CreateForm(FlaskForm):
    productID = StringField(_l('Product ID'), validators=[DataRequired()])
    productName = StringField(_l('Product Name'), validators=[DataRequired()])
    price = StringField(_l('Price'), validators=[DataRequired()])
    submit = SubmitField(_l('Create'))

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


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route("/cart")
def cart():
    return render_template("cart.html", title="Home page")

@bp.route("/inventory")
def inventory():
    return render_template("inventory.html", title="Home page")

@bp.route("/home")
def home():
    return render_template("index.html", title="Home page")

@bp.route("/create", methods=['GET', 'POST'])
def create():
    form = CreateForm()
    return render_template('create.html', title='Create', form=form)


