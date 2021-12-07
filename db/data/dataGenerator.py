from faker import Faker
import csv
from werkzeug.security import generate_password_hash
from random import randint
import random
from datetime import datetime, timedelta

# Use faker package for realistic data, some will be overwritten with real data
fake = Faker()

# Create user data
def createUser():
    i = 0
    names = []
    users = []
    while i < 1000:
        firstname = fake.first_name()
        lastname = fake.last_name()
        # enforce only adding unique emails
        if (firstname,lastname) not in names:
            names.append((firstname, lastname))
            user = [i]
            user.append(f"{firstname}.{lastname}@{'gmail.com'}")
            user.append("pbkdf2:sha256:260000$Prs0BucSXtvcysa2$288bd5390da67b596f8dfae36829a51754fd8c1851210d88e79a8946ab7f9592")
            # password is hashed Databosses316!
            user.append(firstname)
            user.append(lastname)
            user.append(fake.street_address())
            user.append("")
            user.append(fake.city())
            user.append(fake.state())
            user.append(fake.postcode())
            users.append(user)
            i +=1
    return users

# Create seller data
def createSeller():
    sellers = []
    sample_users = random.sample(range(0, 999), 200)
    for i in sample_users:
        sellers.append([i])
    return sellers

# Create product data
def createProducts(sellers):
    i = 0
    names = []
    products = []
    while i < 1000:
        product = [i]
        name = fake.word() + " " + fake.word()
        if name not in names:
            names.append(name)
            description = fake.sentence(nb_words=5)
            category = fake.safe_color_name()
            unitPrice = round(random.uniform(00.00, 500.00), 2)
            inventory = randint(0, 1000)
            sellerId = sellers[randint(0, 99)]
            product.append(name)
            product.append(description)
            product.append(category)
            product.append(unitPrice)
            product.append(inventory)
            product.append((sellerId)[0])
            product.append("https://source.unsplash.com/random/200x200/?sig=%d/" % i)
            products.append(product)
            i += 1
    return products

# Create funding data
def createFunding():
    funding = []
    users = random.sample(range(0, 999), 200)
    for i in users:
        fund = [i]
        dt_unformatted = fake.date_time_this_year(True)
        dt = dt_unformatted.strftime('%Y-%m-%d %I:%M:%S %p')
        amount = round(random.uniform(00.00, 500.00), 2)
        fund.append(dt)
        fund.append(amount)
        funding.append(fund)
    x = 500-len(funding) # want 500 entries
    users2 = random.sample(range(0, 999), x)
    for i in users2:
        fund = [i]
        dt = fake.date_time_this_year(True).strftime('%Y-%m-%d %I:%M:%S %p')
        amount = round(random.uniform(00.00, 500.00), 2)
        fund.append(dt)
        fund.append(amount)
        funding.append(fund)
    return funding

# Create purchase data
def createPurchases(funding, products):
    purchases = []
    users = []
    while len(purchases) < 200:
        purchase = []
        user = random.randint(0, 999)
        dt_unformatted = fake.date_time_this_month(True)
        dtplus1 = (dt_unformatted + timedelta(days=1)).strftime('%Y-%m-%d %I:%M:%S %p')
        dt = dt_unformatted.strftime('%Y-%m-%d %I:%M:%S %p')

        funds = 0
        for i in funding:
            if i[0] == user:
                if datetime.strptime(i[1], '%Y-%m-%d %I:%M:%S %p') < dt_unformatted:
                    funds += i[2]
        spent = 0
        for i in purchases:
            if i[1] == user:
                if datetime.strptime(i[3], '%Y-%m-%d %I:%M:%S %p') < dt_unformatted:
                    spent += i[4]
        balance = funds - spent

        productindex = random.randint(0, 199)
        
        if products[productindex][4] <= balance:
            purchase.append(products[productindex][6])
            purchase.append(user)
            purchase.append(products[productindex][0])
            purchase.append(dt)
            purchase.append(products[productindex][4])
            purchase.append(1)
            purchase.append("fulfilled")
            purchase.append(dtplus1)
        if user not in users:
            if purchase != []:
                purchases.append(purchase)
                users.append(user)

    return purchases

# Create cart data
def createCart(products):
    cart = []
    sample_users = random.sample(range(0, 999), 5)
    for i in sample_users:
        productindex = random.randint(0, 199)
        cart.append([i, products[productindex][0], products[productindex][6], 1])
    return cart
    
# Write the data to csvs (include generated in csv name)
if __name__ == '__main__':
    # userData = createUser()
    # with open("db/data/UsersGenerated.csv", "w+") as myCsv:
    #     csvWriter = csv.writer(myCsv, delimiter=',')
    #     csvWriter.writerows(userData)
    
    # sellerData = createSeller()
    # with open("db/data/SellerGenerated.csv", "w+") as myCsv:
    #     csvWriter = csv.writer(myCsv, delimiter=',')
    #     csvWriter.writerows(sellerData)

    # productData = createProducts(sellerData)
    # with open("db/data/ProductsGenerated.csv", "w+") as myCsv:
    #     csvWriter = csv.writer(myCsv, delimiter=',')
    #     csvWriter.writerows(productData)
    
    # fundingData = createFunding()
    # with open("db/data/FundingGenerated.csv", "w+") as myCsv:
    #     csvWriter = csv.writer(myCsv, delimiter=',')
    #     csvWriter.writerows(fundingData)

    # purchasingData = createPurchases(fundingData, productData)
    # with open("db/data/PurchasesGenerated.csv", "w+") as myCsv:
    #     csvWriter = csv.writer(myCsv, delimiter=',')
    #     csvWriter.writerows(purchasingData)
    
    # cartData = createCart(productData)
    # with open("db/data/CartGenerated.csv", "w+") as myCsv:
    #     csvWriter = csv.writer(myCsv, delimiter=',')
    #     csvWriter.writerows(cartData)
    
    
    ### Comment out everything in main func before running this unless you want to generate new data entirely ####
    
    # Before running this, ran productScrape.py to generate clothes.csv file
    # The functions below replace products with real data that we webscraped
    
    random.seed(10)
    
    datafile = open('db/data/ProductsGenerated.csv', 'r')
    datareader = csv.reader(datafile)
    data = []
    for row in datareader:
        data.append(row)    

    datafile = open('db/data/clothes.csv', 'r')
    datareader = csv.reader(datafile)
    scraped = []
    for row in datareader:
        scraped.append(row)    

    for i in range(len(scraped)):
        data[i][1] = scraped[i][0]
        data[i][4] = scraped[i][1]
        data[i][7] = scraped[i][2]

    for i in range(96, 1000):
        data[i][7] = scraped[i % 95][2]

    with open("db/data/ProductsGenerated.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
        
    # Create reviews based on PurchasesGenerated
    for i in data:
        sellersReviews= []
        productReviews= []
        
    with open("db/data/SellerReviewsGenerated.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sellersReviews)
    
    with open("db/data/ProductReviewsGenerated.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(productReviews)
        
    