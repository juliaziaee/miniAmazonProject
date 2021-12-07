from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError


from .. import login

# Create class for balance with the user ID and their overall balance amount
class Balance:
    def __init__(self, id, amount):
        self.id = id
        # Force balance to only have two decimal places
        self.amount = round(amount, 2)

# Function to get a users balance given their user id
    @staticmethod
    def getBalance(id):
        rows = app.db.execute(
            """
SELECT id, amount
FROM userBalance
WHERE id = :id
""",
            id=id,
        )
        return Balance(*(rows[0]))

# Function to updaate user balance given user id, datetime and amount
# Can increase or deduct amount, error handling with a trigger (in create.sql)
# Trigger ensures that the balance cannot go negative (overwithdraw)
    @staticmethod
    def updateBalance(id, transactionDT, amount):
        try:
            app.db.execute(
                """
    INSERT INTO Funding(id, transactionDT, amount)
    VALUES(:id, :transactionDT, :amount)
    RETURNING id
    """,
                id=id,
                amount=amount,
                transactionDT=transactionDT,
            )
        except SQLAlchemyError as e:
            errorInfo = e.orig.args
            error = errorInfo[0]
            return error
        return id

# Create a class for user with id, email, firstname, lastname, address param
class User(UserMixin):
    def __init__(
        self, id, email, firstname, lastname, street1, street2, city, state, zip
    ):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.street1 = street1
        self.street2 = street2
        self.city = city
        self.state = state
        self.zip = zip

# Function to try to login user
    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute(
            """
SELECT password, id, email, firstname, lastname, street1, street2, city, state, zip
FROM Users
WHERE email = :email
""",
            email=email,
        )
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

# Function to check if user email already exists in database
# Used in error checking to prevent email from being non-unique
    @staticmethod
    def email_exists(email):
        rows = app.db.execute(
            """
SELECT email
FROM Users
WHERE email = :email
""",
            email=email,
        )
        return len(rows) > 0
 
 # Function that tells you if a user is a seller given user ID   
    @staticmethod
    def is_seller(id):
        rows = app.db.execute(
            """
SELECT SellerID
FROM Seller
WHERE SellerID = :SellerID
""",
            SellerID=id,
        )
        return len(rows) > 0

# Function to update user email, ensures they give a unique email
    @staticmethod
    def updateEmail(id, email):
        try:
            app.db.execute(
                """
UPDATE Users
SET email = :email
WHERE id = :id
AND NOT EXISTS
    (SELECT *
    FROM Users
    WHERE email = :email)
RETURNING id;""",
                id=id,
                email=email,
            )
        except SQLAlchemyError as e:
            errorInfo = e.orig.args
            error = errorInfo[0]
            return error
        return id

# Functoin to update user password
# Hashes the password that is given on input
    @staticmethod
    def updatePassword(id, newpassword):
        try:
            app.db.execute(
                """
UPDATE Users
SET password = :newpassword
WHERE id = :id
RETURNING id;
""",
                id=id,
                newpassword=generate_password_hash(newpassword),
            )
        except SQLAlchemyError as e:
            errorInfo = e.orig.args
            error = errorInfo[0]
            return error
        return id   

# Function to register a new user, returns User id if successful
# Error checking also happens on the form before registering
    @staticmethod
    def register(
        email, password, firstname, lastname, street1, street2, city, state, zip
    ):
        try:
            rows = app.db.execute(
                """
INSERT INTO Users(email, password, firstname, lastname, street1, street2, city, state, zip)
VALUES(:email, :password, :firstname, :lastname, :street1, :street2, :city, :state, :zip)
RETURNING id
""",
                email=email,
                password=generate_password_hash(password),
                firstname=firstname,
                lastname=lastname,
                street1=street1,
                street2=street2,
                city=city,
                state=state,
                zip=zip,
            )

            id = rows[0][0]
            return User.get(id)
        except Exception:
            return None

# Function to update user info
    @staticmethod
    def update(id, firstname, lastname, street1, street2, city, state, zip):
        try:
            app.db.execute(
                """
                UPDATE Users
                SET firstname = :firstname, lastname = :lastname, street1 = :street1, street2 = :street2, city = :city, state = :state, zip = :zip
                WHERE id = :id
                RETURNING id;""",
                id=id,
                firstname=firstname,
                lastname=lastname,
                street1=street1,
                street2=street2,
                city=city,
                state=state,
                zip=zip,
            )
        except SQLAlchemyError as e:
            errorInfo = e.orig.args
            error = errorInfo[0]
            return error
        return id

# Functoin to load a user given their user ID
    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute(
            """
SELECT id, email, firstname, lastname, street1, street2, city, state, zip
FROM Users
WHERE id = :id
""",
            id=id,
        )
        return User(*(rows[0])) if rows else None
