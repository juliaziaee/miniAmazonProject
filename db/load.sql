# \COPY Users FROM 'data/Users.csv' WITH DELIMITER ',' NULL '' CSV
# \COPY Products FROM 'data/Products.csv' WITH DELIMITER ',' NULL '' CSV
# \COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV

-- populate sample data using insert statements

INSERT INTO Users VALUES
   (1, 'clara.lyra@duke.edu', 'pass1', 'Clara', 'Lyra', 0.00, '123 Erwin Road Durham NC'),
   (2, 'julia.ziaee@duke.edu', 'hhixy', 'Julia', 'Ziaee', 0.00, '300 Swift Ave Durham NC');
 
INSERT INTO Seller VALUES
   (1), (2);
 
INSERT INTO Products VALUES
   (1, 'Game Cube', 'brand new gaming system with controller', 'gaming', 5.0, 1, 2);
 
INSERT INTO Purchases VALUES
   (1, 1, 1, '20210618 10:34:09 AM', 50.00, 1, 'ordered', NULL);
 
INSERT INTO Cart VALUES
   (1, 2, 2, 1),
   (1, 3, 4, 2);
 
INSERT INTO ProductReview VALUES
   (1, 1, 3, 'still waiting on my order but excited', '20210618 09:24:09 AM');
   (1, 1, 3, 'still waiting on my order but excited', '20210618 09:24:09 AM');
 
INSERT INTO SellerReview VALUES
   (1, 1, 1, NULL, '20210611 09:24:09 PM');