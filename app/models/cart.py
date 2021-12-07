from flask import current_app as app
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


class Cart:
    def __init__(self, uid, pid, sid, name, unitPrice, quantity, Inventory, totalPrice, subtotal, imgUrl):
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.name = name
        self.unitPrice = unitPrice
        self.quantity = quantity
        self.Inventory = Inventory
        self.totalPrice = totalPrice
        self.subtotal = subtotal
        self.imgUrl = imgUrl

#get all items in a given user's cart
    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT Cart.uid, Cart.pid, Cart.sid, Products.name, Products.unitPrice, Cart.quantity, Products.Inventory,
    (Cart.quantity * Products.unitPrice) AS totalPrice,
    cartTotalPrice.totalPrice AS subtotal, Products.image AS imgUrl
FROM Cart, Products, cartTotalPrice
WHERE Cart.uid = :uid AND Cart.pid = Products.productID
    AND cartTotalPrice.uid = :uid
''',
                              uid=uid)
        return [Cart(*row) for row in rows]

#  add product at a given quantity to a given user's cart 

    @staticmethod
    def addToCart(uid, pid, sid, quantity):
        try:
            rows = app.db.execute("""
INSERT INTO Cart(uid, pid, sid, quantity)
VALUES(:uid, :pid, :sid, :quantity)
RETURNING pid
""",
                                  uid=uid,
                                  pid=pid,
                                  sid=sid,
                                  quantity = quantity)
            productID = rows[0][0]
            return None
        except Exception:
            return None

#increase or decrease the quantity of a given item in a given user's cart
    @staticmethod
    def updateQuantity(uid, pid, new_quantity):
        try:
            rows = app.db.execute("""
UPDATE Cart
SET quantity = :new_quantity 
WHERE uid = :uid AND pid = :pid
""",
                                  uid=uid,
                                  pid=pid,
                                  new_quantity = new_quantity)
            productID = rows[0][0]
            return None
        except Exception:
            return None

#remove a given item from a given user's cart    
    @staticmethod
    def removeFromCart(uid, pid):
        try:
            rows = app.db.execute("""
DELETE FROM Cart
WHERE uid = :uid AND pid = :pid
""",
                                  uid=uid,
                                  pid=pid)
            productID = rows
            return None
        except Exception:
            return None

#move items from user's cart to purchases table to checkout a cart & delete items from cart upon successful purchase 
    @staticmethod
    def checkoutCart(uid):    
        try:
            orderDateTime = datetime.now()
            rows = app.db.execute('''
                SELECT Cart.uid, Cart.pid, Products.SellerID, Products.unitPrice, Cart.quantity
                FROM Cart, Products
                WHERE Cart.uid = :uid AND Products.productID = Cart.pid
                ''', uid=uid)
        except SQLAlchemyError as e:
            errorInfo = e.orig.args
            error = errorInfo[0].split("CONTEXT")
            return error[0]
        for row in rows:
                res = Cart.insertPurchases(uid, row[1], row[2], row[3], row[4], orderDateTime, orderDateTime)
                if res == uid:
                    Cart.removeFromCart(uid, row[1])
                else:
                    return Cart.insertPurchases(uid, row[1], row[2], row[3], row[4], orderDateTime, orderDateTime)
        return uid

#insert item from cart into purchases table    
    @staticmethod
    def insertPurchases(uid, pid, SellerID, finalUnitPrice, quantity, orderDateTime, fulfillment_datetime):
        fufullmentstatus = "Processing"
        try:
            app.db.execute(
                """
    INSERT INTO Purchases(SellerID, uid, pid, orderDateTime, finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime)
    VALUES(:SellerID, :uid, :pid, :orderDateTime, :finalUnitPrice, :quantity, :fufullmentstatus, :fulfillment_datetime)
    RETURNING uid
    """,
                SellerID = SellerID,
                uid=uid,
                pid=pid,
                orderDateTime=orderDateTime,
                finalUnitPrice=finalUnitPrice,
                quantity=quantity,
                fufullmentstatus=fufullmentstatus,
                fulfillment_datetime=fulfillment_datetime
            )
        except SQLAlchemyError as e:
            errorInfo = e.orig.args
            error = errorInfo[0].split("CONTEXT")
            return error[0]
        return uid
    
   
        
        