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
    def getName(name, description):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND Users.id = Products.SellerID

'''.format(name, description))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategory(category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE category LIKE '%{}%' AND Users.id = Products.SellerID
'''.format(category))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategory(name, description, category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%' AND Users.id = Products.SellerID
'''.format(name, description, category))
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
    def orderAsc():
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE Users.id = Products.SellerID
ORDER BY unitPrice
''')
        return [Product(*row) for row in rows]

    @staticmethod
    def orderDesc():
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE Users.id = Products.SellerID
ORDER BY unitPrice DESC
''')
        return [Product(*row) for row in rows]

    @staticmethod
    def getNameAndAsc(name, description):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND Users.id = Products.SellerID
ORDER BY unitPrice
'''.format(name, description))
        return [Product(*row) for row in rows]

    @staticmethod
    def getNameAndDesc(name, description):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND Users.id = Products.SellerID
ORDER BY unitPrice DESC
'''.format(name, description))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategoryAndAsc(category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE category LIKE '%{}%' AND Users.id = Products.SellerID
ORDER BY unitPrice
'''.format(category))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategoryAndDesc(category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE category LIKE '%{}%' AND Users.id = Products.SellerID
ORDER BY unitPrice DESC
'''.format(category))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategoryAndAsc(name, description, category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%' AND Users.id = Products.SellerID
ORDER BY unitPrice
'''.format(name, description, category))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategoryAndDesc(name, description, category):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%' AND Users.id = Products.SellerID
ORDER BY unitPrice DESC
'''.format(name, description, category))
        return [Product(*row) for row in rows]

    @staticmethod
    def getPrice250(unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID
'''.format(unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getPrice500(unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID
'''.format(unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategoryAndAscAndPrice250(name, description, category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%' AND unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID
ORDER BY unitPrice
'''.format(name, description, category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategoryAndDescAndPrice250(name, description, category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%' AND unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID
ORDER BY unitPrice DESC
'''.format(name, description, category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategoryAndAscAndPrice500(name, description, category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%' AND unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID
ORDER BY unitPrice
'''.format(name, description, category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategoryAndDescAndPrice500(name, description, category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%' AND unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID
ORDER BY unitPrice DESC
'''.format(name, description, category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategoryAndPrice250(name, description, category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%' AND unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID
'''.format(name, description, category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getSearchAndCategoryAndPrice500(name, description, category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND category LIKE '%{}%' AND unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID
'''.format(name, description, category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategoryAndAscAndPrice250(category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE category LIKE '%{}%' AND unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID
ORDER BY unitPrice
'''.format(category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategoryAndAscAndPrice500(category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE category LIKE '%{}%' AND unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID
ORDER BY unitPrice
'''.format(category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategoryAndDescAndPrice250(category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE category LIKE '%{}%' AND unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID
ORDER BY unitPrice DESC
'''.format(category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategoryAndDescAndPrice500(category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE category LIKE '%{}%' AND unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID
ORDER BY unitPrice DESC
'''.format(category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategoryAndPrice250(category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE category LIKE '%{}%' AND unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID
'''.format(category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getCategoryAndPrice500(category, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE category LIKE '%{}%' AND unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID
'''.format(category, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getNameAndAscAndPrice250(name, description, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID
ORDER BY unitPrice
'''.format(name, description, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getNameAndAscAndPrice500(name, description, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID
ORDER BY unitPrice
'''.format(name, description, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getNameAndDescAndPrice250(name, description, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID
ORDER BY unitPrice DESC
'''.format(name, description, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getNameAndDescAndPrice500(name, description, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID
ORDER BY unitPrice DESC
'''.format(name, description, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getNameAndPrice250(name, description, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID

'''.format(name, description, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def getNameAndPrice500(name, description, unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE (name LIKE '%{}%' OR description LIKE '%{}%') AND unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID

'''.format(name, description, unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def orderAscAndPrice250(unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID
ORDER BY unitPrice
'''.format(unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def orderAscAndPrice500(unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID
ORDER BY unitPrice
'''.format(unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def orderDescAndPrice250(unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE unitPrice > 0 AND unitPrice <= 250 AND Users.id = Products.SellerID
ORDER BY unitPrice DESC
'''.format(unitPrice))
        return [Product(*row) for row in rows]

    @staticmethod
    def orderDescAndPrice500(unitPrice):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, rating, SellerID, firstname
FROM Products LEFT OUTER JOIN ProductReview ON Products.productID = ProductReview.pid, Users
WHERE unitPrice > 250 AND unitPrice <= 500 AND Users.id = Products.SellerID
ORDER BY unitPrice DESC
'''.format(unitPrice))
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