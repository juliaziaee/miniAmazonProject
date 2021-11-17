from flask import current_app as app
from flask import Flask, render_template

class Product:
    def __init__(self, id, name, price, image, category, description, Inventory, rating):
        self.id = id
        self.name = name
        self.price = price
        self.image = image
        self.category = category
        self.description = description
        self.Inventory = Inventory
        self.rating = rating

    @staticmethod
    def get(productID):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
WHERE productID = :productID
''',
                              productID=productID)
        return Product(*(rows[0])) if rows is not [] else []

    @staticmethod
    def getName(name, description):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
WHERE (name LIKE '%{}%' OR description LIKE '%{}%')

'''.format(name, description))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategory(category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
WHERE category LIKE '%{}%'
'''.format(category))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategory(name, description, category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%'
'''.format(name, description, category))
        return [Product(*row) for row in rows]

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
''',)
        return [Product(*row) for row in rows]

    @staticmethod
    def orderAsc():
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
ORDER BY unitPrice
''')
        return [Product(*row) for row in rows]

    @staticmethod
    def orderDesc():
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
ORDER BY unitPrice DESC
''')
        return [Product(*row) for row in rows]

    @staticmethod
    def getNameAndAsc(name, description):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
WHERE (name LIKE '%{}%' OR description LIKE '%{}%')
ORDER BY unitPrice
'''.format(name, description))
        return [Product(*row) for row in rows]

    @staticmethod
    def getNameAndDesc(name, description):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
WHERE (name LIKE '%{}%' OR description LIKE '%{}%')
ORDER BY unitPrice DESC
'''.format(name, description))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategoryAndAsc(category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
WHERE category LIKE '%{}%'
ORDER BY unitPrice
'''.format(category))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategoryAndDesc(category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
WHERE category LIKE '%{}%'
ORDER BY unitPrice DESC
'''.format(category))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategoryAndAsc(name, description, category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%'
ORDER BY unitPrice
'''.format(name, description, category))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategoryAndDesc(name, description, category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%'
ORDER BY unitPrice DESC
'''.format(name, description, category))
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