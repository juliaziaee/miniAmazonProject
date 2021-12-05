from flask import current_app as app


class Orders:
    def __init__(self, uid, sellerID, pid, street1, street2, city, state, zip1, orderDateTime,
finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime, totalPrice):
        self.uid = uid
        self.sellerID = sellerID
        self.pid = pid
        self.street1 = street1
        self.street2 = street2
        self.city = city
        self.state = state
        self.zip = zip1
        self.orderDateTime = orderDateTime
        self.finalUnitPrice = finalUnitPrice
        self.quantity = quantity
        self.fufullmentstatus = fufullmentstatus
        self.fulfillment_datetime = fulfillment_datetime
        self.totalPrice = totalPrice


    @staticmethod
    def get(seller):
        # buyer information including address, date order placed,
        # total amount/number of items, and overall fulfillment status
        rows = app.db.execute('''
SELECT uid, sellerID, pid, street1, street2, city, state, zip, orderDateTime,
finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime, SUM(finalUnitPrice) as totalPrice
FROM Purchases, Users
WHERE Purchases.uid = Users.id AND Purchases.SellerID = :SellerID
GROUP BY uid, sellerID, pid, street1, street2, city, state, zip, orderDateTime,
finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime
ORDER BY orderDateTime DESC
''',
                              SellerID=seller)
        return [Orders(*row) for row in rows]


    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT Purchases.uid, sellerID, pid, street1, street2, city, state, zip, orderDateTime,
finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime, SUM(finalUnitPrice) as totalPrice
FROM Purchases, Users
WHERE Purchases.uid = Users.id
ORDER BY orderDateTime DESC
''',)
        return [Orders(*row) for row in rows]
    
    @staticmethod
    def getOrders(uid):
        # buyer information including address, date order placed,
        # total amount/number of items, and overall fulfillment status
        rows = app.db.execute('''
SELECT *
FROM Purchases
WHERE uid = :uid
ORDER BY orderDateTime DESC
''',
                              uid=uid)
        return [Orders(*row) for row in rows]
