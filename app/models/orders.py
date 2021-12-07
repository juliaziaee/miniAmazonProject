from flask import current_app as app
from flask_login import current_user


class Orders:
    def __init__(self, uid, sellerID, pid, street1, street2, city, state, zip1, orderDateTime,
finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime, totalPrice, productName, reviewStatus):
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
        self.productName = productName
        self.reviewStatus = reviewStatus


#get a given seller's orders
    @staticmethod
    def get(seller):
        # buyer information including address, date order placed,
        # total amount/number of items, and overall fulfillment status
        rows = app.db.execute('''
SELECT Purchases.uid, Purchases.SellerID, pid, street1, street2, city, state, zip, orderDateTime,
finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime, 
(quantity*finalUnitPrice) AS totalPrice, Products.name AS productName, ''
FROM Purchases, Users, Products
WHERE Purchases.uid = Users.id AND Purchases.SellerID = :SellerID AND Products.productID = Purchases.pid
ORDER BY orderDateTime DESC
''',
                              SellerID=seller)
        return [Orders(*row) for row in rows]

#get a given seller's orders from a given individual
    @staticmethod
    def getIndividual(seller, uid, orderDateTime):
        # buyer information including address, date order placed,
        # total amount/number of items, and overall fulfillment status
        rows = app.db.execute('''
SELECT Purchases.uid, Purchases.SellerID, pid, street1, street2, city, state, zip, orderDateTime,
finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime, 
(quantity*finalUnitPrice) AS totalPrice, Products.name AS productName, ''
FROM Purchases, Users, Products
WHERE Purchases.uid = Users.id AND Purchases.SellerID = :SellerID AND Products.productID = Purchases.pid AND Users.id = :uid AND
orderDateTime = :orderDateTime
ORDER BY fulfillment_datetime DESC
''',
                              SellerID=seller, uid = uid, orderDateTime = orderDateTime)
        return [Orders(*row) for row in rows]

#get an overview of the seller's items sold
    @staticmethod
    def getOverview(seller):
        rows = app.db.execute('''
SELECT Purchases.uid, Purchases.SellerID, '', street1, street2, city, state, zip, orderDateTime,
SUM(finalUnitPrice * quantity), SUM(quantity), ARRAY_AGG(DISTINCT fufullmentstatus) fufullmentstatuses, MAX(fulfillment_datetime), 
'', '', ''
FROM Purchases, Users
WHERE Purchases.uid = Users.id AND Purchases.SellerID = :SellerID
GROUP BY Purchases.uid, Purchases.SellerID, street1, street2, city, state, zip, orderDateTime
ORDER BY orderDateTime DESC
''',
                              SellerID=seller)
        return [Orders(*row) for row in rows]

#get all orders that exist
    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT Purchases.uid, Purchases.SellerID, pid, street1, street2, city, state, zip, orderDateTime,
finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime, 
(quantity*finalUnitPrice) AS totalPrice, Products.name AS productName, ''
FROM Purchases, Users, Products
WHERE Purchases.uid = Users.id AND Products.productID = Purchases.pid
ORDER BY orderDateTime DESC
''')
        return [Orders(*row) for row in rows]

#get all items from a given user's/buyer's specific order    
    @staticmethod
    def getSingleOrder(uid, orderDateTime):
        # buyer information including address, date order placed,
        # total amount/number of items, and overall fulfillment status
        rows = app.db.execute('''
SELECT Purchases.uid, Purchases.SellerID, Purchases.pid, street1, street2, city, state, zip, orderDateTime,
finalUnitPrice, quantity, fufullmentstatus, fulfillment_datetime, 
(quantity*finalUnitPrice) AS totalPrice, Products.name AS productName, ''
FROM Purchases, Users, Products
WHERE Purchases.uid = Users.id AND Purchases.uid = :uid 
    AND Products.productID = Purchases.pid AND Purchases.orderDateTime = :orderDateTime
ORDER BY orderDateTime DESC
''',
                              uid=uid,
                              orderDateTime=orderDateTime)
        return [Orders(*row) for row in rows]

#get all orders for a given user/buyer    
    @staticmethod
    def getOrders(uid):
        rows = app.db.execute('''
SELECT Purchases.uid, '', '', street1, street2, city, state, zip, orderDateTime,
SUM(finalUnitPrice * quantity), SUM(quantity), ARRAY_AGG(DISTINCT fufullmentstatus) fufullmentstatuses, MAX(fulfillment_datetime), 
'', '', ''
FROM Purchases, Users, Products
WHERE Purchases.uid = :uid AND Users.id = :uid AND Products.productID = Purchases.pid
GROUP BY orderDateTime, Purchases.uid, street1, street2, city, state, zip
ORDER BY orderDateTime DESC
''',
                              uid=uid)
        return [Orders(*row) for row in rows]

#mark item order as fulfilled in purchases
    @staticmethod
    def markFulfilled(uid, sellerID, orderDateTime, pid):
        try:
            rows = app.db.execute("""
UPDATE Purchases
SET fufullmentstatus = 'fulfilled', fulfillment_datetime = LOCALTIMESTAMP(0)
WHERE uid = :uid AND SellerID = :sellerID AND orderDateTime = :orderDateTime AND pid = :pid
""",
                                  uid = uid, sellerID = sellerID, orderDateTime = orderDateTime, pid = pid)

            return None
        except Exception:
            return None

#find a buyer's given order
    @staticmethod
    def getSearchAndFilt(searchBuyer, searchDate):

        if searchBuyer:

            query = '''
SELECT Purchases.uid, Purchases.SellerID, '', street1, street2, city, state, zip, orderDateTime,
SUM(finalUnitPrice * quantity), SUM(quantity), ARRAY_AGG(DISTINCT fufullmentstatus) fufullmentstatuses, MAX(fulfillment_datetime), 
'', '', ''
FROM Purchases, Users
WHERE Purchases.uid = Users.id AND Purchases.SellerID = :SellerID AND Users.id = :searchBuyer
GROUP BY Purchases.uid, Purchases.SellerID, street1, street2, city, state, zip, orderDateTime
'''

        else:
            query = '''
SELECT Purchases.uid, Purchases.SellerID, '', street1, street2, city, state, zip, orderDateTime,
SUM(finalUnitPrice * quantity), SUM(quantity), ARRAY_AGG(DISTINCT fufullmentstatus) fufullmentstatuses, MAX(fulfillment_datetime), 
'', '', ''
FROM Purchases, Users
WHERE Purchases.uid = Users.id AND Purchases.SellerID = :SellerID
GROUP BY Purchases.uid, Purchases.SellerID, street1, street2, city, state, zip, orderDateTime
'''
        if searchDate == "dateNew":
            query += "ORDER BY orderDateTime DESC"
        if searchDate == "dateOld":
            query += "ORDER BY orderDateTime"
                
        rows = app.db.execute(query,
searchBuyer = searchBuyer,
SellerID = current_user.id
)
        return [Orders(*row) for row in rows]

#get a buyer's given order
    @staticmethod
    def getOrders(uid):
        rows = app.db.execute('''
SELECT Purchases.uid, '', '', street1, street2, city, state, zip, orderDateTime,
SUM(finalUnitPrice * quantity), SUM(quantity), ARRAY_AGG(DISTINCT fufullmentstatus) fufullmentstatuses, MAX(fulfillment_datetime), 
'', '', ''
FROM Purchases, Users, Products
WHERE Purchases.uid = :uid AND Users.id = :uid AND Products.productID = Purchases.pid
GROUP BY orderDateTime, Purchases.uid, street1, street2, city, state, zip
ORDER BY orderDateTime DESC
''',
                              uid=uid)
        return [Orders(*row) for row in rows]


#analytics for sellers
class Stats:
    def __init__(self, uid, quantity, spent):
        self.uid = uid
        self.quantity = quantity
        self.spent = spent

#get a seller's analytics
    @staticmethod
    def stats(seller):
        # buyer information including address, date order placed,
        # total amount/number of items, and overall fulfillment status
        rows = app.db.execute('''
SELECT Purchases.uid, SUM(quantity), SUM(finalUnitPrice * quantity) as tot
FROM Purchases, Users
WHERE Purchases.uid = Users.id AND Purchases.SellerID = :SellerID
GROUP BY Purchases.uid, Purchases.SellerID
ORDER BY tot DESC
''',
                              SellerID=seller)
        return [Stats(*row) for row in rows]

#filter for a buyer's activity
    @staticmethod
    def getSearchAndFilt(searchBuyer, searchTotal, searchUnits):

        if searchBuyer:

            query = '''
SELECT Purchases.uid, SUM(quantity) as units, SUM(finalUnitPrice * quantity) as tot
FROM Purchases, Users
WHERE Purchases.uid = Users.id AND Purchases.SellerID = :SellerID AND Users.id = :searchBuyer
GROUP BY Purchases.uid, Purchases.SellerID
'''

        else:
            query = '''
SELECT Purchases.uid, SUM(quantity) as units, SUM(finalUnitPrice * quantity) as tot
FROM Purchases, Users
WHERE Purchases.uid = Users.id AND Purchases.SellerID = :SellerID
GROUP BY Purchases.uid, Purchases.SellerID
'''
        if searchTotal == "totalMost":
            query += "ORDER BY tot DESC"
        if searchTotal == "totalLeast":
            query += "ORDER BY tot"

        if searchUnits == "unitsMost":
            query += "ORDER BY units DESC"
        if searchUnits == "unitsLeast":
            query += "ORDER BY units"
                
        rows = app.db.execute(query,
searchBuyer = searchBuyer,
SellerID = current_user.id
)
        return [Stats(*row) for row in rows]
