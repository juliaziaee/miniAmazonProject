from flask import current_app as app
from flask import Flask, render_template
from sqlalchemy.exc import SQLAlchemyError

# Create a class for product information
class Product:
    def __init__(self, id, name, price, image, category, description, Inventory, sellerID, sellerName):
        self.id = id
        self.name = name
        self.price = price
        self.image = image
        self.category = category
        self.description = description
        self.Inventory = Inventory
        self.sellerID = sellerID
        self.sellerName = sellerName

    # Function to return product information given a product ID 
    @staticmethod
    def get(productID):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, SellerID, firstname
FROM Products, Users
WHERE productID = :productID AND Users.id = Products.SellerID
''',
                              productID=productID)
        return Product(*(rows[0])) if rows else None

    # Function to select distinct categories from database
    def addCategory():
        rows = app.db.execute('''
SELECT DISTINCT(category)
FROM Products
''')    
        data = []
        for row in rows:
            data.append(str(str(row)[2:-3]))
        return data

    # Function gets specific products after filtering and sorting 
    @staticmethod
    def getSearchAndFilt(category, keyword, sort, price):
        category = "%{}%".format(category)
        keyword = "%{}%".format(keyword)
        
        query = '''
SELECT productID, name, unitPrice, image, category, description, Inventory, SellerID, firstname
FROM Products, Users
WHERE (name LIKE :keyword OR description LIKE :keyword) AND (category LIKE :category) AND Users.id = Products.SellerID
'''
        if price == "0":
            query += "AND unitPrice <= 100"
        if price == "100":
            query += "AND unitPrice > 100 AND unitPrice < 200"
        if price == "200":
            query += "AND unitPrice > 200 AND unitPrice < 300"
        if price == "300":
            query += "AND unitPrice > 300 AND unitPrice < 400"
        if price == "400":
            query += "AND unitPrice > 400 AND unitPrice < 500"
        if price == "over":
            query += "AND unitPrice > 500"
            
        if sort == "Low":
            query += "ORDER BY unitPrice"
        if sort == "High":
            query += "ORDER BY unitPrice DESC"
        if sort == "idlow":
            query += "ORDER BY productID"
        if sort == "idhigh":
            query += "ORDER BY productID DESC"
        if sort == "quantlow":
            query += "ORDER BY Inventory"
        if sort == "quanthigh":
            query += "ORDER BY Inventory DESC"
                
        rows = app.db.execute(query,
category=category,
keyword=keyword,
)
        return [Product(*row) for row in rows]

    # Function that gets all available products
    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image, category, description, Inventory, SellerID, firstname
FROM Products, Users
WHERE Users.id = Products.SellerID
''',)
        return [Product(*row) for row in rows]

    # Function that checks if the product exists
    @staticmethod
    def product_exists(productID):
        rows = app.db.execute("""
SELECT productID
FROM Products
WHERE productID = :productID
""",
                              productID=productID)
        return len(rows) > 0

    # Function that checks if seller exists
    @staticmethod
    def seller_exists(SellerID):
        rows = app.db.execute("""
SELECT SellerID
FROM Seller
WHERE SellerID = :SellerID
""",
                              SellerID=SellerID)
        return len(rows) > 0

    # Function that adds a seller to the seller table
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

    # Function that creates a new product and inserts into product table
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
        
    # Function to update product info, only ever gets called if that user is the seller who listed the product
    @staticmethod
    def update(pid, name, description, category, unitPrice, inventory, image):
        try:
            rows = app.db.execute(
                """
                UPDATE Products
                SET name = :name, description = :description, category = :category, unitPrice = :unitPrice, Inventory = :inventory, image = :image
                WHERE productID = :pid
                RETURNING productID""",
                pid=pid,
                name=name,
                description=description,
                category=category,
                unitPrice=unitPrice,
                inventory=inventory,
                image=image)
        # Intercept error
        except SQLAlchemyError as e:
            errorInfo = e.orig.args
            error = errorInfo[0]
            return error
        productID = rows[0][0]
        return productID