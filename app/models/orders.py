from flask import current_app as app


class Orders:
    def __init__(self, id, name, num_in_stock, seller):
        self.id = id
        self.name = name
        self.num_in_stock = num_in_stock
        self.seller = seller

    @staticmethod
    def get(seller):
        # buyer information including address, date order placed,
        # total amount/number of items, and overall fulfillment status
        rows = app.db.execute('''
SELECT uid, street1, street2, city, state, zip, orderDateTime,
finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime
FROM Purchases, Users
WHERE Purchases.uid = Users.id AND Purchases.SellerID = :SellerID
''',
                              SellerID=seller)
        return [Orders(*row) for row in rows]

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT Purchases.uid, street1, street2, city, state, zip, orderDateTime,
finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime
FROM Purchases, Users
WHERE Purchases.uid = Users.id
''',)
        return [Orders(*row) for row in rows]
