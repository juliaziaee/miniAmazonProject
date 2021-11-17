from flask import render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_login import current_user
from flask_paginate import Pagination, get_page_args
import datetime

from .models.inventory import Inventory
from .models.cart import Cart
from .models.product import Product
from .models.orders import Orders
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('products', __name__)

class CreateForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    ## add word limit
    description = StringField(_l('Product Description'), validators=[DataRequired()])
    ## add dropdown menu
    category = StringField(_l('Category'), validators=[DataRequired()])
    unitPrice = StringField(_l('Unit Price'), validators=[DataRequired()])
    num_products = StringField(_l('Number of Units'), validators=[DataRequired()])
    image = StringField(_l('Image URL'), validators=[DataRequired()])
    submit = SubmitField(_l('Create'))

@bp.route("/create", methods=['GET', 'POST'])
def create():
    form = CreateForm()
    ## check user logged in, product id not in use, and populate database
    ## create product id????
    if current_user.is_authenticated:
        if form.validate_on_submit():
            if Product.create(form.name.data,
                            form.description.data,
                            form.category.data,
                            form.unitPrice.data,
                            form.num_products.data,
                            current_user.id,
                            form.image.data):
                                flash('Congratulations, you have listed an item!')
                                return redirect(url_for('users.login'))
        return render_template('create.html', title='Create', form=form)
    else:
        return redirect(url_for('users.login'))

@bp.route("/cart")
def cart():
    if current_user.is_authenticated:
        #get current items in user's cart
        cart = Cart.get(current_user.id)
    else:
        #not logged in so redirect to login page 
        return redirect(url_for('users.login'))
    #ender page by adding ingo to the index.html file
    return render_template("cart.html", 
                                cart_items=cart)

@bp.route("/inventory")
def inventory():
    if current_user.is_authenticated:
        # get all available products for sale:
        inventory = Inventory.get(current_user.id)
        # render the page by adding information to the index.html file
        return render_template('inventory.html',
                           avail_inventory=inventory)
    else:
        return redirect(url_for('users.login'))


@bp.route("/orders")
def orders():
    if current_user.is_authenticated:
        # get all available products for sale:
        orders = Orders.get(current_user.id)
        # render the page by adding information to the index.html file
        return render_template('orders.html',
                           order_history=orders)
    else:
        return redirect(url_for('users.login'))

def get_products(products, offset=0, per_page=10):
    return products[offset: offset + per_page]

@bp.route("/search",  methods = ['POST', 'GET'])
def search():
    c = request.args.get('c')
    q = request.args.get('q')
    s = request.args.get('s')
    p = request.args.get('p')
    if c and q and s and p:
        if s == "Low" and p == "250":
            products = Product.getSearchAndCategoryAndAscAndPrice250(q,q,c,p)
        elif s == "High" and p == "250":
            products = Product.getSearchAndCategoryAndDescAndPrice250(q,q,c,p)
        elif s == "Low" and p == "500":
            products = Product.getSearchAndCategoryAndAscAndPrice500(q,q,c,p)
        elif s == "High" and p == "500":
            products = Product.getSearchAndCategoryAndDescAndPrice500(q,q,c,p)
        elif s == "Low" and p == "N/A":
            products = Product.getSearchAndCategoryAndAsc(q,q,c)
        elif s == "High" and p == "N/A":
            products = Product.getSearchAndCategoryAndDesc(q,q,c)
        elif s == "N/A" and p == "250":
            products = Product.getSearchAndCategoryAndPrice250(q,q,c,p)
        elif s == "N/A" and p == "500":
            products = Product.getSearchAndCategoryAndPrice500(q,q,c,p)
        else:
            products = Product.getSearchAndCategory(q,q,c)
    elif c and s and p:
        if s == "Low" and p == "250":
            products = Product.getCategoryAndAscAndPrice250(c,p)
        elif s == "High" and p == "250":
            products = Product.getCategoryAndDescAndPrice250(c,p)
        elif s == "Low" and p == "500":
            products = Product.getCategoryAndAscAndPrice500(c,p)
        elif s == "High" and p == "500":
            products = Product.getCategoryAndDescAndPrice500(c,p)
        elif s == "Low" and p == "N/A":
            products = Product.getCategoryAndAsc(c)
        elif s == "High" and p == "N/A":
            products = Product.getCategoryAndDesc(c)
        elif s == "N/A" and p == "250":
            products = Product.getCategoryAndPrice250(c,p)
        elif s == "N/A" and p == "500":
            products = Product.getCategoryAndPrice500(c,p)
        else:
            products = Product.getCategory(c)
    elif q and s and p:
        if s == "Low" and p == "250":
            products = Product.getNameAndAscAndPrice250(q,q,p)
        elif s == "High" and p == "250":
            products = Product.getNameAndDescAndPrice250(q,q,p)
        elif s == "Low" and p == "500":
            products = Product.getNameAndAscAndPrice500(q,q,p)
        elif s == "High" and p == "500":
            products = Product.getNameAndDescAndPrice500(q,q,p)
        elif s == "Low" and p == "N/A":
            products = Product.getNameAndAsc(q,q)
        elif s == "High" and p == "N/A":
            products = Product.getNameAndDesc(q,q)
        elif s == "N/A" and p == "250":
            products = Product.getNameAndPrice250(q,q,p)
        elif s == "N/A" and p == "500":
            products = Product.getNameAndPrice500(q,q,p)
        else:
            products = Product.getName(q,q)
    elif s and p:
        if s == "Low" and p == "250":
            products = Product.orderAscAndPrice250(p)
        elif s == "High" and p == "250":
            products = Product.orderDescAndPrice250(p)
        elif s == "Low" and p == "500":
            products = Product.orderAscAndPrice500(p)
        elif s == "High" and p == "500":
            products = Product.orderDescAndPrice500(p)
        elif s == "Low" and p == "N/A":
            products = Product.orderAsc()
        elif s == "High" and p == "N/A":
            products = Product.orderDesc()
        elif s == "N/A" and p == "250":
            products = Product.getPrice250(p)
        elif s == "N/A" and p == "500":
            products = Product.getPrice500(p)
        else:
            products = Product.get_all(True)
    elif c:
        products = Product.getCategory(c)
    elif q:
        products = Product.getName(q,q)
    else:
        products = Product.get_all(True)

        # get all available products for sale:
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(products)
    pagination_products = get_products(products, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file

    return render_template('index.html', 
                           products=pagination_products,
                           page = page,
                           per_page = per_page,
                           pagination = pagination,
                           purchase_history=purchases,
                           )