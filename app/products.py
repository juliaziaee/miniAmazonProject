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
from .models.orders import Stats
from .models.reviews import ProdReviews
from .models.purchase import Purchase
from .models.saved import Saved

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
    if current_user.is_authenticated:
        if form.validate_on_submit():
            if Product.create(form.name.data,
                            form.description.data,
                            form.category.data,
                            form.unitPrice.data,
                            form.num_products.data,
                            current_user.id,
                            form.image.data):
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


@bp.route("/inventory/<int:pid>/<int:num>")
def updateInventoryQty(pid, num):
    #change inventory in database
    Inventory.updateQuantity(pid,num)
    #refresh page
    return redirect(url_for('products.inventory'))
    

@bp.route("/cart/<int:pid>")
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


@bp.route("/detailview/<int:id>")
def detailview(id):
    if current_user.is_authenticated:
        return render_template('detailview.html', product = Product.get(id),

                                                  user = current_user.id,
                                                  availBought = Purchase.hasPurchased(current_user.id, id),
                                                  availNew = ProdReviews.hasReviewed(current_user.id, id),

                                                  averageReview = ProdReviews.getAvgReview(id),
                                                  review = ProdReviews.get_all(id),
                                                  leng = len(ProdReviews.get_all(id)))
    else:
        return redirect(url_for('users.login'))


class ReviewForm(FlaskForm):
    review = StringField(_l('Review'), validators=[DataRequired()])
    ## add dropdown menu
    rating = SelectField(_l('Rating'), choices=[1,2,3,4,5], validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

@bp.route("/newReview/<int:id>", methods=["GET", "POST"])
def review(id):
    form = ReviewForm()
    if form.validate_on_submit():
        if ProdReviews.NewProdReview(
            current_user.id, 
            id,
            form.review.data,
            form.rating.data,
        ):        
            return redirect(url_for('products.detailview', id= id))
    return render_template("newReview.html", title="Leave a Product Review", form=form)

class updateReviewForm(FlaskForm):
    review = StringField(_l('Review'), validators=[DataRequired()])
    rating = SelectField(_l('Rating'), choices=[1,2,3,4,5], validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

@bp.route("/updateReview/<int:id>", methods=["GET", "POST"])
def updatereview(id):
    form = updateReviewForm()
    if form.validate_on_submit():
        if ProdReviews.updateProdReview(
            current_user.id, 
            id,
            form.review.data,
            form.rating.data,
        ):        
            return redirect(url_for('products.detailview', id= id))
    return render_template("updateReview.html", title="Edit Your Product Review", form=form)

@bp.route("/detailview/remove/<pid>/<uid>")
def removereview(uid, pid):
    ProdReviews.removeProdReviews(uid, pid)
    return redirect(url_for('products.detailview', id= pid))

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


@bp.route("/sellerAnalytics")
def sellerAnalytics():
    if current_user.is_authenticated:
        # get all available products for sale:
        orders = Orders.get(current_user.id)
        stats = Stats.stats(current_user.id)
        # render the page by adding information to the index.html file
        return render_template('selleranalytics.html', orders = orders, stats = stats)
    else:
        return redirect(url_for('users.login'))


@bp.route("/inventory/<pid>")
def removeinventory(pid):
    Inventory.removeInventory(pid)
    #ender page by adding ingo to the index.html file
    return redirect(url_for('products.inventory'))

@bp.route("/detailview/<int:pid>/<int:numVotes>/<int:uid>/up")
def upVotes(pid, numVotes, uid):
    #change inventory in database
    ProdReviews.upVotes(pid, numVotes, uid)
    #refresh page
    return redirect(url_for('products.detailview', id = pid))

@bp.route("/detailview/<int:pid>/<int:numVotes>/<int:uid>/down")
def downVotes(pid, numVotes, uid):
    #change inventory in database
    ProdReviews.downVotes(pid,numVotes, uid)
    #refresh page
    return redirect(url_for('products.detailview', id = pid))

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

@bp.route("/orders/<int:uid>/<int:sellerID>/<orderDateTime>/<int:pid>")
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
    products = Product.getSearchAndFilt(c, q, s, p)

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

@bp.route("/orderssearch",  methods = ['POST', 'GET'])
def orderssearch():
    searchBuyer = request.args.get('searchBuyer')
    searchDate = request.args.get('searchDate')
    orders = Orders.getSearchAndFilt(searchBuyer, searchDate)
    # render the page by adding information to the index.html file

    return render_template('orders.html', 
                           order_history=orders
                           )

@bp.route("/analyticssearch",  methods = ['POST', 'GET'])
def analyticssearch():
    searchBuyer = request.args.get('searchBuyer')
    searchTotal = request.args.get('searchTotal')
    searchUnits = request.args.get('searchUnits')
    orders = Stats.getSearchAndFilt(searchBuyer, searchTotal, searchUnits)
    # render the page by adding information to the index.html file

    return render_template('selleranalytics.html', 
                           stats=orders
                           )

# Create a flask form to edit product information
class EditForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Product Description'), validators=[DataRequired()])
    category = SelectField(_l('Category'), choices=data, validators=[DataRequired()])
    unitPrice = StringField(_l('Unit Price'), validators=[DataRequired()])
    num_products = StringField(_l('Number of Units'), validators=[DataRequired()])
    image = StringField(_l('Image URL'), validators=[DataRequired()])
    update = SubmitField(_l('Update'))

# Function to edit product
@bp.route("/edit/<int:pid>", methods=['GET', 'POST'])
def edit(pid):
    product = Product.get(pid)
    options = Product.addCategory()
    for i in options:
        if i not in data:
            data.append(i)
    data.sort()
    form = EditForm() 
    error = None
    # if the user is logged in, otherwise make them login
    if current_user.is_authenticated:
        if form.validate_on_submit():
            # If its successful, should return product ID
            if Product.update(pid,
                            form.name.data,
                            form.description.data,
                            form.category.data,
                            form.unitPrice.data,
                            form.num_products.data,
                            form.image.data) == pid:
                                return redirect(url_for('products.inventory'))
            # If there is an error, display it
            else: error = Product.update(pid,
                            form.name.data,
                            form.description.data,
                            form.category.data,
                            form.unitPrice.data,
                            form.num_products.data,
                            form.image.data)
        # In the edit.html template, only displays the form to update product if your userid matches the
        # user ID of the person who listed the product (the seller)
        return render_template('edit.html', title='Update', form=form, product=product, error=error)
    else:
        return redirect(url_for('users.login'))

# Function for saved to later additional feature
@bp.route("/savedforlater")
def savedForLater():
    if current_user.is_authenticated:
        # get all orders
        savedItems = Saved.getSaved(current_user.id)
        # render the page by adding information to the saved.html file
        return render_template('savedItems.html',
                           saved_items=savedItems)
    else:
        return redirect(url_for('users.login'))

# Function to remove items from saved for later
@bp.route("/savedforlater/remove/<int:pid>")
def removeItemSaved(pid):
    if current_user.is_authenticated:
        #get current items in user's cart
        Saved.removeSavedItem(current_user.id, pid)
    else:
        #not logged in so redirect to login page 
        return redirect(url_for('users.login'))
    #refresh page
    return redirect(url_for('products.savedForLater'))


# Function to move a saved for later item to the cart
@bp.route("/savedforlater/tocart/<int:pid>/<int:sid>")
def savedToCart(pid,sid):
    if current_user.is_authenticated:
        #add entry to cart
        Cart.addToCart(current_user.id, pid,sid, 1)
        #remove from saved for later since its now in cart
        Saved.removeSavedItem(current_user.id, pid)
    else:
        #not logged in so redirect to login page 
        return redirect(url_for('users.login'))
    #ender page by adding ingo to the index.html file
    return redirect(url_for('products.displaycart'))

# Function to move a item from cart to saved for later
@bp.route("/savedforlater/tosaved/<int:pid>/<int:sid>")
def cartToSaved(pid, sid):
    if current_user.is_authenticated:
        #add entry to cart
        Saved.addToSaved(current_user.id, pid, sid)
        #remove from saved for later since its now in cart
        Cart.removeFromCart(current_user.id, pid)
    else:
        #not logged in so redirect to login page 
        return redirect(url_for('users.login'))
    #ender page by adding ingo to the index.html file
    return redirect(url_for('products.displaycart'))
