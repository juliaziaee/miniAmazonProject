from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, name, unitPrice, quantity, totalPrice, subtotal):
        self.uid = uid
        self.pid = pid
        self.name = name
        self.unitPrice = unitPrice
        self.quantity = quantity
        self.totalPrice = totalPrice
        self.subtotal = subtotal

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT Cart.uid, Cart.pid, Products.name, Products.unitPrice, Cart.quantity, 
    (Cart.quantity * Products.unitPrice) AS totalPrice,
    cartTotalPrice.totalPrice AS subtotal
FROM Cart, Products, cartTotalPrice
WHERE Cart.uid = :uid AND Cart.pid = Products.productID
    AND cartTotalPrice.uid = :uid
''',
                              uid=uid)
        return [Cart(*row) for row in rows]

#     @staticmethod
#     def get_all(available=True):
#         rows = app.db.execute('''
# SELECT productID, name, inventory, SellerID
# FROM Products
# ''',)
#         return [Inventory(*row) for row in rows]