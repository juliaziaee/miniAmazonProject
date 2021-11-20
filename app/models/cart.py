from flask import current_app as app


class Cart:
    def __init__(self, uid, pid, name, unitPrice, quantity, Inventory, totalPrice, subtotal, imgUrl):
        self.uid = uid
        self.pid = pid
        self.name = name
        self.unitPrice = unitPrice
        self.quantity = quantity
        self.Inventory = Inventory
        self.totalPrice = totalPrice
        self.subtotal = subtotal
        self.imgUrl = imgUrl

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT Cart.uid, Cart.pid, Products.name, Products.unitPrice, Cart.quantity, Products.Inventory,
    (Cart.quantity * Products.unitPrice) AS totalPrice,
    cartTotalPrice.totalPrice AS subtotal, Products.image AS imgUrl
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
            # likely id already in use; better error checking and
            # reporting needed
            return None