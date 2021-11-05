from flask import render_template
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

from flask import Blueprint
bp = Blueprint('products', __name__)

class CreateForm(FlaskForm):
    productID = StringField(_l('Product ID'), validators=[DataRequired()])
    productName = StringField(_l('Product Name'), validators=[DataRequired()])
    price = StringField(_l('Price'), validators=[DataRequired()])
    submit = SubmitField(_l('Create'))

@bp.route("/create", methods=['GET', 'POST'])
def create():
    form = CreateForm()
    return render_template('create.html', title='Create', form=form)

@bp.route("/cart")
def cart():
    return render_template("cart.html", title="Home page")

@bp.route("/inventory")
def inventory():
    return render_template("inventory.html", title="Home page")