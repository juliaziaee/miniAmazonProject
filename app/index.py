from flask import render_template
from flask_login import current_user
import datetime
from flask_paginate import Pagination, get_page_args

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__)

def get_products(products, offset=0, per_page=10):
    return products[offset: offset + per_page]


@bp.route('/')
def index():
    # get all available products for sale:
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    products = Product.get_all(True)
    total = len(products)
    pagination_products = get_products(products, offset=offset, per_page=per_page)
    print(pagination_products)
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
