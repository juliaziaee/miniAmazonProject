from flask import current_app as app
from flask import Flask, render_template

class Product:
    def __init__(self, id, name, price, image, category, description, Inventory, rating, sellerID, sellerName):
        self.id = id
        self.name = name
        self.price = price
        self.image = image
        self.category = category
        self.description = description
        self.Inventory = Inventory
        self.rating = rating
        self.sellerID = sellerID
        self.sellerName = sellerName

    @staticmethod
    def get(productID):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE productID = :productID AND Users.id = Products.SellerID
''',
                              productID=productID)
        return Product(*(rows[0])) if rows is not [] else []

    def addCategory():
        rows = app.db.execute('''
SELECT DISTINCT(category)
FROM Products
''')    
        data = []
        for row in rows:
            data.append(str(str(row)[2:-3]))
        return data

    @staticmethod
    def getSearchAndFilt(category, keyword, sort, price):
        category = "%{}%".format(category)
        keyword = "%{}%".format(keyword)
        
        query = '''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE :keyword OR description LIKE :keyword) AND (category LIKE :category) AND Users.id = Products.SellerID
'''
        if price == "250":
            query += "AND unitPrice < 250"
        if price == "500":
            query += "AND unitPrice > 250 AND unitPrice < 500"
        if price == "over":
            query += "AND unitPrice > 500"
            
        if sort == "Low":
            query += "ORDER BY unitPrice"
        if sort == "High":
            query += "ORDER BY unitPrice DESC"
                
        rows = app.db.execute(query,
category=category,
keyword=keyword,
)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE Users.id = Products.SellerID
''',)
        return [Product(*row) for row in rows]

    @staticmethod
    def product_exists(productID):
        rows = app.db.execute("""
SELECT productID
FROM Products
WHERE productID = :productID
""",
                              productID=productID)
        return len(rows) > 0

    @staticmethod
    def seller_exists(SellerID):
        rows = app.db.execute("""
SELECT SellerID
FROM Seller
WHERE SellerID = :SellerID
""",
                              SellerID=SellerID)
        return len(rows) > 0

    @staticmethod
    def add_seller(SellerID):
        try:
            rows = app.db.execute("""
INSERT INTO Seller(SellerID)
VALUES(:SellerID)
""",
                                  SellerID = SellerID)
            return [Seller(*row) for row in rows]
        except Exception:
            return None

    @staticmethod
    def create(name, description, category, unitPrice, inventory, SellerID, image):
        if not Product.seller_exists(SellerID):
            Product.add_seller(SellerID)
        try:
            rows = app.db.execute("""
INSERT INTO Products(name, description, category, unitPrice, inventory, SellerID, image)
VALUES(:name, :description, :category, :unitPrice, :inventory, :SellerID, :image)
RETURNING productID
""",
                                  name=name,
                                  description=description,
                                  category=category,
                                  unitPrice = unitPrice,
                                  inventory = inventory,
                                  SellerID = SellerID,
                                  image = image)
            productID = rows[0][0]
            return Product.get(productID)
        except Exception:
            # likely id already in use; better error checking and
            # reporting needed
            return None