from flask import current_app as app
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


class Saved:
    def __init__(self, uid, pid, sid, name, unitPrice, Inventory, imgUrl):
        self.uid = uid
        self.sid = sid
        self.pid = pid
        self.name = name
        self.unitPrice = unitPrice
        self.Inventory = Inventory
        self.imgUrl = imgUrl
    
    @staticmethod
    def getSaved(uid):
        rows = app.db.execute('''
SELECT SavedItems.uid, SavedItems.pid, SavedItems.sid, Products.name, Products.unitPrice, 
    Products.Inventory, Products.image AS imgUrl
FROM SavedItems, Products
WHERE SavedItems.uid = :uid AND SavedItems.pid = Products.productID
''',
                              uid=uid)
        return [Saved(*row) for row in rows]
    
    @staticmethod
    def removeSavedItem(uid, pid):
        try:
            rows = app.db.execute("""
DELETE FROM SavedItems
WHERE uid = :uid AND pid = :pid
""",
                                  uid=uid,
                                  pid=pid)
            return None
        except Exception:
            # likely id already in use; better error checking and
            # reporting needed
            return None
    
    @staticmethod
    def addToSaved(uid, pid, sid):
        try:
            rows = app.db.execute("""
INSERT INTO SavedItems(uid, pid, sid)
VALUES(:uid, :pid, :sid)
RETURNING pid
""",
                                  uid=uid,
                                  pid=pid,
                                  sid=sid)
            productID = rows[0][0]
            return None
        except Exception:
            # likely id already in use; better error checking and
            # reporting needed
            return None
    
