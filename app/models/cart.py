from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, name, quantity, totalPrice):
        self.uid = uid
        self.pid = pid
        self.name = name
        self.quantity = quantity
        self.totalPrice = totalPrice

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT Cart.uid, Cart.pid, Products.name, Cart.quantity, 
    (Cart.quantity * Products.unitPrice) AS totalPrice
FROM Cart, Products
WHERE Cart.uid = :uid AND Cart.pid = Products.productID
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