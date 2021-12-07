from flask import current_app as app


class Purchase:
    def __init__(self, uid, sellerid, pid, orderDateTime):
        self.uid = uid
        self.sellerid = sellerid
        self.pid = pid
        self.orderDateTime = orderDateTime

#get purchases for a given user 
    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid, sellerid, pid, orderDateTime
FROM Purchases
WHERE uid = :uid
''',
                              uid=uid)
        return Purchase(*(rows[0])) if rows else None

#get all orders for a given user since a certain date
    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT uid, sellerid, pid, orderDateTime
FROM Purchases
WHERE uid = :uid
AND orderDateTime >= :since
ORDER BY orderDateTime DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

#check if user has purchased item already
    @staticmethod
    def hasPurchased(uid, pid):
        if app.db.execute('''
SELECT uid, pid
FROM Purchases
WHERE uid = :uid and pid = :pid
''',
                              uid=uid,
                              pid = pid):
            return True
        else:
            return False

#check if user has purchased from seller already
    @staticmethod
    def hasPurchasedS(SellerID, uid):
        if app.db.execute('''
SELECT SellerID, uid
FROM Purchases
WHERE uid = :uid and SellerID = :SellerID
''',
                              uid=uid,
                              SellerID = SellerID):
            return True
        else:
            return False

#select categories of items user has purchased        
    @staticmethod
    def get_by_category(uid):
        rows = app.db.execute('''
SELECT category, SUM(finalUnitPrice*quantity)
FROM Purchases, Products
WHERE uid = :uid
AND Products.productID = Purchases.pid
GROUP BY category
''',
                              uid=uid)
        return str(rows)
