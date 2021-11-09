from flask import current_app as app


class Inventory:
    def __init__(self, id, name, num_in_stock, seller):
        self.id = id
        self.name = name
        self.num_in_stock = num_in_stock
        self.seller = seller

    @staticmethod
    def get(seller):
        rows = app.db.execute('''
SELECT productID, name, inventory, SellerID
FROM Products
WHERE SellerID = :SellerID
''',
                              SellerID=seller)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT productID, name, inventory, SellerID
FROM Products
''',)
        return [Inventory(*row) for row in rows]
