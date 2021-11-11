from flask import current_app as app


class Product:
    def __init__(self, id, name, price, image):
        self.id = id
        self.name = name
        self.price = price
        self.image = image

    @staticmethod
    def get(productID):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image
FROM Products
WHERE productID = :productID
''',
                              productID=productID)
        return Product(*(rows[0])) if rows is not [] else []

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, image
FROM Products
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