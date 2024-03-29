from typing import Type
from flask import render_template, redirect, url_for, flash, request, session
from flask.app import Flask
import datetime
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    EqualTo,
    Length
)
from flask_babel import _, lazy_gettext as _l
from datetime import datetime
import re

from .models.user import User
from .models.user import Balance
from .models.orders import Orders
from .models.purchase import Purchase
from .models.reviews import SellerReviews
from .models.reviews import ProdReviews
from .models.purchase import Purchase
from .models.product import Product


from flask import Blueprint

bp = Blueprint("users", __name__)

# Create a flask form that users use to login with email and password credentials
class LoginForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Sign In"))

# Create a function to login a user
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        # Error if the user logs in with invalid credentials
        if user is None:
            flash("Invalid email or password", "login")
            return redirect(url_for("users.login"))
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)

# Create a flask form that users use to register as a new user
class RegistrationForm(FlaskForm):
    firstname = StringField(_l("First Name"), validators=[DataRequired()])
    lastname = StringField(_l("Last Name"), validators=[DataRequired()])
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    password2 = PasswordField(
        _l("Repeat Password"), validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField(_l("Register"))
    street1 = StringField(_l("Street Line 1"), validators=[DataRequired()])
    street2 = StringField(_l("Street Line 2"))
    city = StringField(_l("City"), validators=[DataRequired()])
    state = StringField(_l("State"), validators=[DataRequired()])
    zip = StringField(
        _l("Postal Code"), validators=[DataRequired(), Length(min=5, max=5)]
    )
    
    # Made sure zip code is 5 digit number
    def validate_zip(form, field):
        try:
            float(field.data)
        except ValueError:
            raise ValidationError("Must be a valid zipcode")

    # Enforce user registering with email not previously used
    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError(_("Already a user with this email."))

# Function to register a new user
@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(
            form.email.data,
            form.password.data,
            form.firstname.data,
            form.lastname.data,
            form.street1.data,
            form.street2.data,
            form.city.data,
            form.state.data,
            form.zip.data,
        ):
            flash("Congratulations, you are now a registered user! Sign in with your credentials!", "login")
            return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)

# Create flask form to update user email
class UpdateEmailForm(FlaskForm):
    email = StringField(_l("New Email Address"), validators=[DataRequired(), Email()])
    submit = SubmitField(_l("Update Email"))

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError(_("Already a user with this email."))

# Function to update user email
@bp.route("/updateemail", methods=["GET", "POST"])
def updateemail():
    error = None
    # if user is authenticated use their id and let them update email
    if current_user.is_authenticated:
        form = UpdateEmailForm()
        if form.validate_on_submit():
            if User.updateEmail(current_user.id, form.email.data) == current_user.id:
                return redirect(url_for("users.accountdetails"))
            else:
                # if the function fails, show the error message
                error = User.updateEmail(current_user.id, form.email.data).split(
                    "CONTEXT"
                )[0]
        return render_template(
            "updateemail.html", title="Account Balance", error=error, form=form
        )
    else:
        return render_template("updateemail.html", title="Account Balance")

# Create flask form to update password
class UpdatePasswordForm(FlaskForm):
    new_password = PasswordField(_l("New Password"), validators=[DataRequired()])
    # repeat password to enforce they match
    new_password2 = PasswordField(
        _l("Repeat New Password"), validators=[DataRequired(), EqualTo("new_password")]
    )
    submit = SubmitField(_l("Update Password"))

# 
@bp.route("/updatepassword", methods=["GET", "POST"])
def updatepassword():
    error = None
    if current_user.is_authenticated:
        form = UpdatePasswordForm()
        if form.validate_on_submit():
            if (
                User.updatePassword(current_user.id, form.new_password.data)
                == current_user.id
            ):
                return redirect(url_for("users.accountdetails"))
            else:
                error = User.updatePassword(
                    current_user.id, form.new_password.data
                ).split("CONTEXT")[0]
        return render_template(
            "updatepassword.html", title="Update Password", form=form, error=error
        )
    else:
        return render_template("updateemail.html", title="Account Balance")

# Create flask form for user to update details
class UpdateUserInfoForm(FlaskForm):
    firstname = StringField(_l("First Name"), validators=[DataRequired()])
    lastname = StringField(_l("Last Name"), validators=[DataRequired()])
    street1 = StringField(_l("Street Line 1"), validators=[DataRequired()])
    street2 = StringField(_l("Street Line 2"))
    city = StringField(_l("City"), validators=[DataRequired()])
    state = StringField(_l("State"), validators=[DataRequired()])
    zip = StringField(
        _l("Postal Code"), validators=[DataRequired(), Length(min=5, max=5)]
    )
    submit = SubmitField(_l("Update"))
    
    # Enforce valid zip code
    def validate_zip(form, field):
        try:
            float(field.data)
        except ValueError:
            raise ValidationError("Must be a valid zipcode")
            
# Function to update user info
@bp.route("/updateuserinfo", methods=["GET", "POST"])
def updateuserinfo():
    error = None
    # if the user is authenticated let them update details
    if current_user.is_authenticated:
        form = UpdateUserInfoForm()
        if form.validate_on_submit():
            if (
                User.update(
                    current_user.id,
                    form.firstname.data,
                    form.lastname.data,
                    form.street1.data,
                    form.street2.data,
                    form.city.data,
                    form.state.data,
                    form.zip.data,
                )
                == current_user.id
            ):
                return redirect(url_for("users.accountdetails"))
            # if sql error show the error message
            else:
                error = User.update(
                    current_user.id,
                    form.firstname.data,
                    form.lastname.data,
                    form.street1.data,
                    form.street2.data,
                    form.city.data,
                    form.state.data,
                    form.zip.data,
                ).split("CONTEXT")[0]
        return render_template(
            "updateuserinfo.html", title="Update Info", form=form, error=error
        )
    else:
        return render_template("updateuserinfo.html", title="Update Info")

# Create flask form for users to add/deduct funds from their aaccount
class FundsForm(FlaskForm):
    amount = DecimalField(_l("Amount"))
    submit = SubmitField(_l("Submit"))

    # Make sure the amount has no more than two decimal places
    def validate_amount(form, field):
        if "." in (str(field.data)):
            x = (str(field.data)).split(".")[1]
            if len(x) > 2:
                raise ValidationError("Cannot exceed two decimal places")

# Function to update account balace
@bp.route("/accountbalance", methods=["GET", "POST"])
def accountbalance():
    error = None
    # User must be authenticated
    if current_user.is_authenticated:
        # Retreive current balance
        userbal = Balance.getBalance(current_user.id)
        form = FundsForm()
        if form.validate_on_submit():
            if (
                Balance.updateBalance(
                    current_user.id,
                    datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
                    form.amount.data,
                )
                == current_user.id
            ):
                return redirect(url_for("users.accountbalance"))
            # Show error if fails. Ex. trigger error if deduct more balance than you have
            else:
                error = (
                    Balance.updateBalance(
                        current_user.id,
                        datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
                        form.amount.data,
                    ).split("CONTEXT")
                )[0]
        return render_template(
            "accountbalance.html",
            title="Account Balance",
            balance=userbal,
            form=form,
            error=error,
        )
    else:
        return render_template("accountbalance.html", title="Account Balance")

# Creatae function to show account details page
@bp.route("/accountdetails")
def accountdetails():
    return render_template("accountdetails.html", title="Home page", review = ProdReviews.get_authored(current_user.id), reviewS = SellerReviews.get_authored(current_user.id))

# Create function to show user details page (Public View for user)
@bp.route("/userdetails/<int:uid>", methods=["GET", "POST"])
def userdetails(uid):
    if User.is_seller(uid):
        rateVal = ProdReviews.getAvgSellerReview(uid)
    else:
        rateVal = 0
    if current_user.is_authenticated:
        return render_template('userdetails.html',page = User.get(uid),
                                                  seller = User.is_seller(uid),
                                                  user = current_user.id,
                                                  availBought = Purchase.hasPurchasedS(uid, current_user.id),
                                                  availNew = SellerReviews.hasReviewedS(current_user.id, uid),
                                                  review = SellerReviews.get_user_reviews(uid),
                                                  leng = len(SellerReviews.get_user_reviews(uid)),
                                                  avgRating = rateVal)
    else:
        return redirect(url_for('users.login'))

# Create form to review a seller
class SellerReviewForm(FlaskForm):
    review = StringField(_l('Review'), validators=[DataRequired()])
    ## add dropdown menu
    rating = SelectField(_l('Rating'), choices=[1,2,3,4,5], validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

#  Function to show seller reviews
@bp.route("/newSellerReview/<int:id>", methods=["GET", "POST"])
def review(id):
    form = SellerReviewForm()
    if form.validate_on_submit():
        if SellerReviews.NewSellerReview(
            current_user.id, 
            id,
            form.review.data,
            form.rating.data,
        ):        
            return redirect(url_for('users.userdetails', uid= id))
    return render_template("newSellerReview.html", title="Leave a Seller Review", form=form)

# Create form to update existing seller reviews
class updateSellerReviewForm(FlaskForm):
    review = StringField(_l('Review'), validators=[DataRequired()])
    ## add dropdown menu
    rating = SelectField(_l('Rating'), choices=[1,2,3,4,5], validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

# Function to update seller reviews
@bp.route("/editSellerReview/<int:id>", methods=["GET", "POST"])
def updatereview(id):
    form = updateSellerReviewForm()
    if form.validate_on_submit():
        if SellerReviews.updateSellerReview(
            current_user.id, 
            id,
            form.review.data,
            form.rating.data,
        ):        
            return redirect(url_for('users.userdetails', uid= id))
    return render_template("editSellerReview.html", title="Edit Your Seller Review", form=form)

# Function to remove review that a user created
@bp.route("/userdetails/remove/<int:sid>/<int:uid>")
def removereview(sid, uid):
    SellerReviews.removeSellReviews(sid, uid)
    return redirect(url_for('users.userdetails',uid= sid))

# Create function to show order history (overview)
@bp.route("/orderhistory")
def orderhistory():
    if current_user.is_authenticated:
        #get orders if user is logged in 
        orderHist = Orders.getOrders(current_user.id)
    else:
        #prompt user to log in if not
        return redirect(url_for("users.login"))
    #show order history if properly logged in 
    return render_template("orderHistoryOverview.html", order_history = orderHist)

# Function for detailed order history of a specific order
@bp.route("/orderhistory/singleorderhistory/<orderDateTime>")
def singleOrderHistory(orderDateTime):
    if current_user.is_authenticated:
        if len(orderDateTime) > 20:
            format_dateTime = datetime.strptime(orderDateTime, '%Y-%m-%d %H:%M:%S.%f')
        else:
            format_dateTime = datetime.strptime(orderDateTime, '%Y-%m-%d %H:%M:%S')
        #get order details if user is logged in
        orderDetails = Orders.getSingleOrder(current_user.id, format_dateTime)

        #add if review has been made for each order or not
        for i in range(len(orderDetails)):
            orderDetails[i].reviewStatus = ProdReviews.hasReviewed(current_user.id, orderDetails[i].pid)
    else:
        #prompt user to log in if not
        return redirect(url_for("users.login"))
    #show order details if properly logged in 
    return render_template("orderhistory.html", all_orders = orderDetails)

# Create upvotes for reviews
@bp.route("/userdetails/<int:sid>/<numVotes>/<int:uid>/up")
def upVotes(sid, numVotes, uid):
    #change inventory in database
    SellerReviews.upVotesS(sid, numVotes, uid)
    #refresh page
    return redirect(url_for('users.userdetails', uid = sid))

# Create downvotes for reviews
@bp.route("/userdetails/<int:sid>/<numVotes>/<int:uid>/down")
def downVotes(sid, numVotes, uid):
    #change inventory in database
    SellerReviews.downVotesS(sid,numVotes, uid)
    #refresh page
    return redirect(url_for('users.userdetails', uid = sid))

# Show users spending history
@bp.route("/spendinghistory")
def spendinghistory():
    category_purchases = Purchase.get_by_category(current_user.id)
    cat = None
    # if the user has not bought anything, do not try to manipulate category data
    if category_purchases != "[]":
        category_purchases = category_purchases[:-2].split("),")
        cat = []
        for i in category_purchases:
            cat.append(i.split(",")[0][3:-1] + ": $" + str(round(float(i.split(",")[1]),2)))
    return render_template("spendinghistory.html", title="Spending History", cat = cat)

# Logout function when logout button is clicked
@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index.index"))
