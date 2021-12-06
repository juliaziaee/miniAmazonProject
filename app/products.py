from flask import render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_login import current_user
from flask_paginate import Pagination, get_page_args
import datetime

from .models.inventory import Inventory
from .models.cart import Cart
from .models.product import Product
from .models.orders import Orders
from .models.reviews import ProdReviews
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('products', __name__)

options = []
data = []

class CreateForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    ## add word limit
    description = StringField(_l('Product Description'), validators=[DataRequired()])
    ## add dropdown menu
    category = SelectField(_l('Category'), choices=data, validators=[DataRequired()])
    unitPrice = StringField(_l('Unit Price'), validators=[DataRequired()])
    num_products = StringField(_l('Number of Units'), validators=[DataRequired()])
    image = StringField(_l('Image URL'), validators=[DataRequired()])
    submit = SubmitField(_l('Create'))

@bp.route("/create", methods=['GET', 'POST'])
def create():
    options = Product.addCategory()
    for i in options:
        if i not in data:
            data.append(i)
    data.sort()
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

@bp.route("/cart/<int:pid>/<int:sid>/<int:quantity>")
def addtocart(pid,sid,quantity):
    if current_user.is_authenticated:
        #get current items in user's cart
        Cart.addToCart(current_user.id, pid,sid,quantity)
    else:
        #not logged in so redirect to login page 
        return redirect(url_for('users.login'))
    #ender page by adding ingo to the index.html file
    return redirect(url_for('products.displaycart'))

@bp.route("/cart/<int:pid>/<int:quantity>")
def updateCartQty(pid, quantity):
    if current_user.is_authenticated:
        #get current items in user's cart
        Cart.updateQuantity(current_user.id, pid,quantity)
    else:
        #not logged in so redirect to login page 
        return redirect(url_for('users.login'))
    #refresh page
    return redirect(url_for('products.displaycart'))
    

@bp.route("/cart/<pid>")
def removeItem(pid):
    if current_user.is_authenticated:
        #get current items in user's cart
        Cart.removeFromCart(current_user.id, pid)
    else:
        #not logged in so redirect to login page 
        return redirect(url_for('users.login'))
    #refresh page
    return redirect(url_for('products.displaycart'))

@bp.route("/checkout")
def checkout():
    if current_user.is_authenticated:
        #get current items in user's cart & move entries to purchases
        checkedOut = Cart.checkoutCart(current_user.id)
        if checkedOut == current_user.id:
            return render_template('orderSuccess.html')
        else:
            return render_template('orderFail.html', 
                                            error = checkedOut)
    else:
        #not logged in so redirect to login page 
        return redirect(url_for('users.login'))

@bp.route("/displaycart")
def displaycart():
    if current_user.is_authenticated:
        cart = Cart.get(current_user.id)
        total = 0
        for item in cart:
            total += item.totalPrice
    else:
        #not logged in so redirect to login page 
        return redirect(url_for('users.login'))
    #ender page by adding ingo to the index.html file
    return render_template("cart.html", 
                                cart_items=cart,
                                subtotal=total)                     

class ProdReviewForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    email = StringField(_l('Email (will not be published)'), validators=[DataRequired(), Email()])
    review = TextAreaField(_l('Review'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    
@bp.route("/detailview/<int:id>")
def detailview(id):
    if current_user.is_authenticated:
        return render_template('detailview.html', product = Product.get(id),
                                                  user = current_user.id, 
                                                  review = ProdReviews.get_all(id),
                                                  leng = len(ProdReviews.get_all(id)),
                                                  form=ProdReviewForm())
    else:
        return redirect(url_for('users.login'))


class ReviewForm(FlaskForm):
    review = StringField(_l("Review"), validators=[DataRequired()])
    rating = StringField(_l("Rating"), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

@bp.route("/newReview/<int:id>", methods=["GET", "POST"])
def review(id):
    form = ReviewForm()
    user = current_user.id
    product = Product.get(id)
    if form.validate_on_submit():
        if ProdReviews.NewProdReview(
            user, 
            product, 
            form.review.data,
            form.rating.data,
        ):
        
            flash("You have successfully submitted a review!")
            return redirect(url_for("product.detailview"))
    return render_template("newReview.html", title="Leave a Review", form=form)

@bp.route("/individualOrder/<int:uid>/<int:sellerID>/<orderDateTime>")
def individualOrder(uid, sellerID, orderDateTime):
    return render_template('individualorder.html', order_history = Orders.getIndividual(current_user.id, uid, orderDateTime))

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

@bp.route("/inventory/<pid>")
def removeinventory(pid):
    Inventory.removeInventory(pid)
    #ender page by adding ingo to the index.html file
    return redirect(url_for('products.inventory'))


@bp.route("/orders")
def orders():
    if current_user.is_authenticated:
        # get all orders
        orders = Orders.getOverview(current_user.id)
        # render the page by adding information to the orders.html file
        return render_template('orders.html',
                           order_history=orders)
    else:
        return redirect(url_for('users.login'))

@bp.route("/orders/<uid>/<sellerID>/<orderDateTime>/<pid>")
def markFulfilled(uid, sellerID, orderDateTime, pid):
    Orders.markFulfilled(uid, sellerID, orderDateTime, pid)
    return redirect(url_for('products.individualOrder', uid = uid, sellerID = sellerID, orderDateTime = orderDateTime))

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
        elif s == "Low" and p == "over":
            products = Product.getSearchAndCategoryAndAscAndPriceOver500(q,q,c,p)
        elif s == "High" and p == "over":
            products = Product.getSearchAndCategoryAndDescAndPriceOver500(q,q,c,p)
        elif s == "Low" and p == "N/A":
            products = Product.getSearchAndCategoryAndAsc(q,q,c)
        elif s == "High" and p == "N/A":
            products = Product.getSearchAndCategoryAndDesc(q,q,c)
        elif s == "N/A" and p == "250":
            products = Product.getSearchAndCategoryAndPrice250(q,q,c,p)
        elif s == "N/A" and p == "500":
            products = Product.getSearchAndCategoryAndPrice500(q,q,c,p)
        elif s == "N/A" and p == "over":
            products = Product.getSearchAndCategoryAndPriceOver500(q,q,c,p)
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
        elif s == "Low" and p == "over":
            products = Product.getCategoryAndAscAndPriceOver500(c,p)
        elif s == "High" and p == "over":
            products = Product.getCategoryAndDescAndPriceOver500(c,p)
        elif s == "Low" and p == "N/A":
            products = Product.getCategoryAndAsc(c)
        elif s == "High" and p == "N/A":
            products = Product.getCategoryAndDesc(c)
        elif s == "N/A" and p == "250":
            products = Product.getCategoryAndPrice250(c,p)
        elif s == "N/A" and p == "500":
            products = Product.getCategoryAndPrice500(c,p)
        elif s == "N/A" and p == "over":
            products = Product.getCategoryAndPriceOver500(c,p)
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
        elif s == "Low" and p == "over":
            products = Product.getNameAndAscAndPriceOver500(q,q,p)
        elif s == "High" and p == "over":
            products = Product.getNameAndDescAndPriceOver500(q,q,p)
        elif s == "Low" and p == "N/A":
            products = Product.getNameAndAsc(q,q)
        elif s == "High" and p == "N/A":
            products = Product.getNameAndDesc(q,q)
        elif s == "N/A" and p == "250":
            products = Product.getNameAndPrice250(q,q,p)
        elif s == "N/A" and p == "500":
            products = Product.getNameAndPrice500(q,q,p)
        elif s == "N/A" and p == "over":
            products = Product.getNameAndPriceOver500(q,q,p)
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
        elif s == "Low" and p == "over":
            products = Product.orderAscAndPriceOver500(p)
        elif s == "High" and p == "over":
            products = Product.orderDescAndPriceOver500(p)
        elif s == "Low" and p == "N/A":
            products = Product.orderAsc()
        elif s == "High" and p == "N/A":
            products = Product.orderDesc()
        elif s == "N/A" and p == "250":
            products = Product.getPrice250(p)
        elif s == "N/A" and p == "500":
            products = Product.getPrice500(p)
        elif s == "N/A" and p == "over":
            products = Product.getPriceOver500(p)
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