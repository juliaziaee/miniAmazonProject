from flask import render_template
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_login import current_user

from .models.inventory import Inventory

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
    # get all available products for sale:
    inventory = Inventory.get(current_user.id)
    # render the page by adding information to the index.html file
    return render_template('inventory.html',
                           avail_inventory=inventory)