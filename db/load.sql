-- populate sample data using csvs

\COPY Users FROM 'data/UsersGenerated.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq', 1000, false);
\COPY Seller FROM 'data/SellerGenerated.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'data/ProductsGenerated.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_productID_seq', 1000, false);
\COPY Funding FROM 'data/FundingGenerated.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'data/PurchasesGenerated.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Cart FROM 'data/CartGenerated.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SellerReview FROM 'data/SellerReviewsGenerated.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ProductReview FROM 'data/ProductReviewsGenerated.csv' WITH DELIMITER ',' NULL '' CSV