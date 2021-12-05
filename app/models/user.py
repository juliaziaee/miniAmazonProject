from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError


from .. import login

class Balance:
    def __init__(self, id, amount):
        self.id = id
        self.amount = round(amount,2)

    @staticmethod
    def getBalance(id):
        rows = app.db.execute("""
SELECT id, amount
FROM userBalance
WHERE id = :id
""",
            id=id)
        return Balance(*(rows[0]))

    @staticmethod
    def updateBalance(id, transactionDT, amount):
        try: app.db.execute("""
    INSERT INTO Funding(id, transactionDT, amount)
    VALUES(:id, :transactionDT, :amount)
    RETURNING id
    """,
                id=id,
                amount=amount,
                transactionDT=transactionDT)
        except SQLAlchemyError as e:
            errorInfo = e.orig.args
            error = (errorInfo[0])
            return error
        return id
            


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, street1, street2, city, state, zip):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.street1 = street1
        self.street2 = street2
        self.city = city
        self.state = state
        self.zip = zip

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, street1, street2, city, state, zip
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, street1, street2, city, state, zip):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, street1, street2, city, state, zip)
VALUES(:email, :password, :firstname, :lastname, :street1, :street2, :city, :state, :zip)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname,
                                  lastname=lastname,
                                  street1 = street1,
                                  street2 = street2,
                                  city = city,
                                  state = state,
                                  zip = zip)

            id = rows[0][0]
            return User.get(id)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    def update(id, email, firstname, lastname, street1, street2, city, state, zip):
            try:
                app.db.execute("""
                UPDATE Users
                SET email = :email, firstname = :firstname, lastname = :lastname, street1 = :street1, street2 = :street2, city = :city, state = :state, zip = :zip
                WHERE id = :id
                AND NOT EXISTS
                    (SELECT *
                    FROM Users
                    WHERE email = :email)
                RETURNING id;""",
                                    id=id,
                                    email=email,
                                    firstname=firstname,
                                    lastname=lastname,
                                    street1=street1,
                                    street2=street2,
                                    city=city,
                                    state=state,
                                    zip=zip)
                return id
            except Exception:
                return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, street1, street2, city, state, zip
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None
