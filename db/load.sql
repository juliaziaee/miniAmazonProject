-- populate sample data using csvs

\COPY Users FROM 'data/Users.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Seller FROM 'data/Seller.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'data/Products.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Cart FROM 'data/Cart.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SellerReview FROM 'data/SellerReview.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ProductReview FROM 'data/ProductReview.csv' WITH DELIMITER ',' NULL '' CSV

-- populate sample data using insert statements (does not conflict with above data)

INSERT INTO Users VALUES
   (1, 'clara.lyra@duke.edu', 'pass1', 'Clara', 'Lyra', '123 Erwin Road', NULL, 'Durham', 'NC', '27705'),
   (2, 'julia.ziaee@duke.edu', 'hhixy', 'Julia', 'Ziaee', '300 Swift Ave', NULL, 'Durham', 'NC', '27705');
 
INSERT INTO Seller VALUES
   (1), (2);

INSERT INTO Products VALUES
   (1, 'Game Cube', 'brand new gaming system with controller', 'gaming', 5.00, 1, 2);
 
INSERT INTO Purchases VALUES
   (2, 1, 1, '20210618 10:34:09 AM', 5.00, 1, 'ordered', NULL);
 
INSERT INTO Cart VALUES
   (1, 1, 2, 1);
 
INSERT INTO ProductReview VALUES
   (1, 1, 3, 'still waiting on my order but excited', '20210618 09:24:09 AM');
 
INSERT INTO SellerReview VALUES
   (1, 2, 1, NULL, '20210611 09:24:09 PM');
   
INSERT INTO SellerReview VALUES
   (2, 5, 4, NULL, '20210611 09:24:09 PM');