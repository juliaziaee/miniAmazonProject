--Holds user information and balance
CREATE TABLE Users (
    id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    firstname VARCHAR(256) NOT NULL,
    lastname VARCHAR(256) NOT NULL,
    street1 VARCHAR(256) NOT NULL, 
    street2 VARCHAR(256), 
    city VARCHAR(256) NOT NULL, 
    state VARCHAR(256) NOT NULL, 
    zip INT NOT NULL
);

-- Keeps track of which users are sellers
CREATE TABLE Seller (
    SellerID INT NOT NULL PRIMARY KEY, 
    FOREIGN KEY (SellerID) REFERENCES Users(id)
);

-- Table to store product offerings and their inventory status by seller
CREATE TABLE Products (
    productID INT NOT NULL,
    name VARCHAR(256) UNIQUE NOT NULL,
    description VARCHAR(256) NOT NULL,
    category VARCHAR(256) NOT NULL,
    unitPrice FLOAT NOT NULL,
    CHECK(unitPrice > 0.0),
    Inventory INT NOT NULL,
    CHECK(Inventory > -1),
    SellerID INT NOT NULL,
    PRIMARY KEY(productID),
    FOREIGN KEY(SellerID) REFERENCES Seller(SellerID) 
);

-- Table to keep track of purchases/order history and the price at which units were purchased
-- Makes hard copy of unit price since a product's price can change (i.e. doesn't reference products for price)
CREATE TABLE Purchases (
    SellerID INT NOT NULL,
    FOREIGN KEY (SellerID) REFERENCES Seller(SellerID),
    uid INT NOT NULL,
    FOREIGN KEY (uid) REFERENCES Users(id),
    pid INT NOT NULL,
    FOREIGN KEY (pid) REFERENCES Products(productID),
    orderDateTime timestamp without time zone NOT NULL DEFAULT (current_timestamp AT  TIME ZONE 'UTC'),
    finalUnitPrice FLOAT ,
	quantity INT NOT NULL,
    CHECK(quantity >= 1), 
    fufullmentstatus VARCHAR(256) NOT NULL, 
    fulfillment_datetime timestamp without time zone, 
    PRIMARY KEY(SellerID, uid, pid, orderDateTime)
);
 
-- Keeps track of what items are in a given user's cart
CREATE TABLE Cart (
	uid INT NOT NULL REFERENCES USERS(id),
	pid INT NOT NULL,
	sid INT NOT NULL REFERENCES SELLER(SellerId),
	quantity INT NOT NULL,
	CHECK(quantity >= 1),
	PRIMARY KEY(uid, pid, sid)
);
 
-- Stores user reviews on a product
-- Will need to create a trigger to ensure that user can only review a product they actually purchased
CREATE TABLE ProductReview (
	uid INT NOT NULL REFERENCES USERS(id),
	pid INT NOT NULL REFERENCES PRODUCTS(productID),
	rating FLOAT NOT NULL,
	CHECK (rating >= 1.0 AND rating <= 5.0),
	review VARCHAR(256),
	DateTime timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
	PRIMARY KEY(uid, pid)
);
 
-- Stores user's reviews on a given seller
-- Will need a trigger to check that user has actually purchased and received a fulfilled order from seller
CREATE TABLE SellerReview (
	uid INT NOT NULL REFERENCES USERS(id),
	sid INT NOT NULL REFERENCES SELLER(SellerId),
	rating FLOAT NOT NULL,
	CHECK(rating >= 1.0 AND rating <= 5.0),
	review VARCHAR(256),
	DateTime timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
	PRIMARY KEY(uid, sid)
	
);

-- Stores conversations between seller and user 
CREATE TABLE Messages (
	uid INT NOT NULL REFERENCES USERS(id),
	sid INT NOT NULL REFERENCES SELLER(SellerId),
	message VARCHAR(256),
	MessageDateTime timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
	PRIMARY KEY(uid, sid, MessageDateTime)
);
 
-- trigger to check that the user has enough in their balance to make a purchase and deducts
-- cost of purchase from balance when possible
CREATE FUNCTION TF_Balance() RETURNS TRIGGER AS $$
BEGIN
 -- check to see if balance is sufficient for purchase
IF EXISTS(SELECT * FROM Users, Purchases
    WHERE uid = NEW.uid AND (NEW.finalUnitPrice * NEW.quantity >= balance)) THEN
    RAISE EXCEPTION 'You do not have enough in your balance to complete this purchase';
END IF;
 -- deduct cost of purchase from balance
IF EXISTS(SELECT * FROM Users, purchases
    WHERE uid = NEW.uid) THEN
    UPDATE balance set balance = balance - (NEW.finalUnitPrice * NEW.quantity);
END IF;
-- Removes items from cart if they have been purchased (i.e. the item is now being moved to purchase table)
IF EXISTS(SELECT * FROM Cart
    WHERE uid = NEW.uid AND pid = NEW.pid)
  THEN
    DELETE FROM Cart WHERE uid = NEW.uid AND pid = NEW.pid;
  END IF;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Ensures there is enough inventory for the user to purchase the item
CREATE FUNCTION TF_Inventory() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS(SELECT * FROM Products, Purchases
        WHERE productID = NEW.uid AND Purchases.SellerID = NEW.SellerID AND inventory- quantity<0) THEN
        RAISE EXCEPTION '% does not have the desired amount in stock', NEW.uid;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
 
-- Checks to see if quantity is valid
CREATE TRIGGER TF_Inventory  
BEFORE INSERT OR UPDATE ON Purchases
  FOR EACH ROW  EXECUTE PROCEDURE TF_Inventory();
 
-- Makes sure user has enough balance to purchase the order and moves items in the order out of their cart
CREATE TRIGGER TG_Balance
BEFORE INSERT ON Purchases
   FOR EACH ROW
   EXECUTE PROCEDURE TF_Balance();

 -- Ensures that customer actually bought product from seller before review
CREATE FUNCTION TF_SellerReview() RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS(SELECT * FROM Purchases
        WHERE uid = NEW.uid AND SellerID = NEW.SellerID) THEN
        RAISE EXCEPTION '% has not purchased a product from %', NEW.uid, NEW.sid;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger checking that reviewer has purchased from seller
CREATE TRIGGER TG_SellerReview
BEFORE INSERT ON SellerReview
    FOR EACH ROW
    EXECUTE PROCEDURE TF_SellerReview();

--  List total cost of all items currently in each users cart
CREATE VIEW cartTotalPrice(uid, totalPrice) AS
    SELECT t2.uid, SUM(t2.itemTotal) AS totalPrice FROM 
        (SELECT Cart.uid, (Cart.quantity * t1.unitPrice) AS itemTotal FROM Cart JOIN 
            (SELECT productId, unitPrice FROM Products) AS t1 ON Cart.pid = t1.productId) AS t2
    GROUP BY t2.uid;
    

 -- Raises error if quantity of an item existing in someones cart is no longer valid because someone
 -- else purchased the item and the inventory is now less than the amount in the user's cart
CREATE FUNCTION TF_validCartQuantity() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS(SELECT * FROM Cart, Products
        WHERE Cart.pid = Products.productID AND Cart.sid = Products.SellerID AND
            Products.productID= NEW.pid AND Products.SellerID = NEW.SellerID AND
            Cart.quantity > Products.inventory) THEN
        RAISE EXCEPTION '% can no longer purchase % units of %', Cart.uid, Cart.quantity, Cart.pid;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger checking that a recent purchase does not make the existing quantity in anyone's carts invalid
CREATE TRIGGER TG_validCartQuantity
AFTER INSERT ON Purchases
    FOR EACH ROW
    EXECUTE PROCEDURE TF_validCartQuantity();

<<<<<<< db/create.sql

TF_updateInventory() RETURNS TRIGGER AS $$
BEGIN
    UPDATE Products set inventory = inventory - NEW.quantity where productID = NEW.pid and SellerID = new.SellerID;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update the product inventory after a purchase
CREATE TRIGGER TG_updateInventory
AFTER INSERT ON Purchases
    FOR EACH ROW
    EXECUTE PROCEDURE TF_updateInventory();

--  Create view page for buyer profile
CREATE VIEW sellerpage(ID) AS
    SELECT sellerID, email, address 
    FROM Seller, Users 
    WHERE ID = uid;


