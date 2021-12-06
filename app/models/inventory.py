from flask import current_app as app


class Inventory:
    def __init__(self, pid, name, num_in_stock, seller):
        self.pid = pid
        self.name = name
        self.num_in_stock = num_in_stock
        self.seller = seller

    @staticmethod
    def get(seller):
        rows = app.db.execute('''
SELECT productID, name, inventory, SellerID
FROM Products
WHERE SellerID = :SellerID AND inventory > 0
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
            # likely id already in use; better error checking and
            # reporting needed
            return None