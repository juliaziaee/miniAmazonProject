from flask import current_app as app


class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT productID, name, unitPrice
FROM Products
WHERE id = :productID
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT productID, name, unitPrice, inventory
FROM Products
''',)
        return [Product(*row) for row in rows]
