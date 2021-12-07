Databosses Mini Amazon Project

Assingment for Duke CS 316

Group Members: 
- Caroline Levenson: Users Guru
- Clara Lyra: Social Guru
- Jennifer Shultz: Products Guru
- Julia Ziaee: Carts Guru
- Nicole Malpeli: Sellers Guru

We chose the standard project option.

Our [Gitlab Repository] (https://gitlab.oit.duke.edu/databosses/mini-amazon-skeleton)

MILESTONE 4 (FINAL)
All members of the group would like to have a group grade.
Final video link: 

To Create and Load Data into Database:
Inside of the VM terminal, cd to the db folder of the final project and run the following commands.
~/shared/final/mini-amazon-skeleton/db$ dropdb amazon; createdb amazon; psql amazon -af create.sql;
~/shared/final/mini-amazon-skeleton/db$ psql amazon -af load.sql

Data Generation:
To create our large test database, we created a python script. In our repo, in our db/data folder there is a file called dataGenerator.py which is the script. To generate the data, you can run this file and then go to the folder db/data (we have already done this). Here you will see a bunch of CSV files we generated. Then in the db folder in the load.sql file we populate our database by loading the generated csv files to our database. We used the \Copy function to load the files into the database. Furthermore, we webscraped in db/data generator.py. If you run this before the generation script, the product information will be written over with real product data that we webscraped.

Progress Report Milestone 3

Video Link: https://duke.zoom.us/rec/share/5kbeXLpq5hiJP2XuVSkErmrx1R9allvSriRIZN9WHHmUgTUOAhlDjLp3bemGpjY0.rhLS1ul8wN6FuTFT?startTime=1636682854000

Contribution Summaries (Milestone 3):
Caroline:
-Wrote most of data generation file and populated the database
-Added funding table to track when user adds and deducts funds from their account
-Added images to be shown on listed products
-Allowed a user to register (then sign in) as a new user -- created form for this and integrated with backend
-Made from and integrated with backend so that a user can update their details, also made one for password
-Showed user balance and allowed them to increment and decrement their balance
Clara:
-Created triggers to limit messaging and reviews to only products that user has purchases or sellers that user has purchased from
-Allows reviews to have a  “thumbs up” and “thumbs down” functionality
-Tested database using sql commands to verify checks and desired functionality
-Populated random product image data
-Started populating messaging data
-Created public view for sellers
Jennifer:
-Added new html document that creates the navigation bars at the top, the dropdowns, and the search bar
-Added routes and href values so that the clicking on the navigation bars will bring user to new page
-Worked on setting up the create product form
-Started implementing the search bar and filtering for specific products be keyword
Julia:
-Reconfigured schema for how to calculate user balances since we added a "Funding" table to keep track of money users add to or remove from their account. Instead of having a table that shows balances, we have a view that adds up the amounts in "Funding" and subtracts the total of all entries in "Purchases" associated with the user's ID
-Made cart page redirect user to login page using routes & href values when user is not logged in but clicks the "cart" tab on the site
-Made cart page display all items in cart associated with logged in user's id (cart contents are 'persistent' as defined in the assignment document)
    -Each row shows product image, product name, product id, unit price, quantity the user wants, and the total price for the item at the user's desired quantity
subtotal row at the bottom shows combined price of all items in user's cart
-Made dynamic 'remove' button for each cart item, dynamic quantity box that can be increased or decreased to a number with maximum 3 digits, and dynamic checkout box that appears below the subtotal 
UI cleanup with CSS file and Javascript script
Nicole:
-Made ‘List’ page with a form in which people can list a new item by inputting product name, description, category, unit price, number of units, and an image URL
-Connected ‘List’ to backend so that when an item is listed the item is shown in the seller’s inventory and in the list of products for sale
-Made random generator for product ids when a user lists a product
-Made it so a user becomes a seller once they list an item
-Made tabs under Seller (Inventory and Orders)
-Redirects users to login page after clicking ‘List’, ‘Inventory’, and ‘Orders’ if user not logged in
-Created orders page that displays the buyer ID, buyer address, date order placed, total amount spent on order, number of items ordered, fulfillment status, and fulfillment date of each order in which an item has been bought from the logged in user
-Insured that inventory and orders are only shown for the logged in user; if the user is not a seller they are prompted to list an item
-Added non-functional update and remove buttons in inventory with ability for seller to change amount in stuck (not yet integrated with backend)


Progress Report Milestone 2

Everyone worked together to sketch an E/R diagram and discuss big picture aspects of the project. 
- Julia spearheaded the creation of the relational schema. 
- Julia and Clara detailed the assumptions and logistics of the schema. 
- Clara and Jennifer focused on specifying the contents and constraints of the main tables. 
- Julia and Nicole focused on creating the triggers for what follows a product purchase. 
- Caroline created inputs for the CSVs to load onto our database.
- Caroline also debugged the SQL database creation and tested the sample data.
- Nicole and Caroline worked on the page by page design on the website. 
