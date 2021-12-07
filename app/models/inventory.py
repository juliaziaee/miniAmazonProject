from flask import current_app as app


class Inventory:
    def __init__(self, pid, name, num_in_stock, seller):
        self.pid = pid
        self.name = name
        self.num_in_stock = num_in_stock
        self.seller = seller

#get products listed for a given seller 
    @staticmethod
    def get(seller):
        rows = app.db.execute('''
SELECT productID, name, inventory, SellerID
FROM Products
WHERE SellerID = :SellerID AND inventory > 0
''',
                              SellerID=seller)
        return [Inventory(*row) for row in rows]

#get all products listed/created
    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT productID, name, inventory, SellerID
FROM Products
''',)
        return [Inventory(*row) for row in rows]

# set inventory to 0 to de-list an item from products available
    @staticmethod
    def removeInventory(pid):
        try:
            rows = app.db.execute("""
UPDATE PRODUCTS
SET Inventory = 0
WHERE productID = :pid
""",
                                  pid = pid)
            return None
        except Exception:
            return None

#change inventory quantity for a given product
    @staticmethod
    def updateQuantity(pid, new_quantity):
        try:
            rows = app.db.execute("""
UPDATE Products
SET Inventory = :new_quantity 
WHERE productID = :pid
""",
                                  pid=pid,
                                  new_quantity = new_quantity)
            return None
        except Exception:
            return None