from faker import Faker
import csv
from werkzeug.security import generate_password_hash
from random import randint
import random
from datetime import datetime, timedelta

fake = Faker()

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
            user.append(generate_password_hash('Databosses316!'))
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

def createSeller():
    sellers = []
    sample_users = random.sample(range(0, 999), 200)
    for i in sample_users:
        sellers.append([i])
    return sellers

def createProducts(sellers):
    i = 0
    names = []
    products = []
    while i < 200:
        product = [i]
        name = fake.word()
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
            product.append("https://source.unsplash.com/random/200x200/?sig=%d/", i)
            products.append(product)
            i += 1
    return products

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
        # if (random.randint(0, 1)) == 1:
        #     deduct = [i]
        #     dtplus1 = dt_unformatted + timedelta(days=1)
        #     if (dtplus1 < datetime.now()):
        #         deduct.append(dtplus1.strftime('%Y-%m-%d %I:%M:%S %p'))
        #         amount2 = -abs(amount)
        #         if (random.randint(0, 1)) == 1:
        #             amount2 = -abs(round(random.uniform(00.00, amount2), 2))
        #         deduct.append(amount2)
        #     funding.append(deduct)
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

def createCart(products):
    cart = []
    sample_users = random.sample(range(0, 999), 5)
    for i in sample_users:
        productindex = random.randint(0, 199)
        cart.append([i, products[productindex][0], products[productindex][6], 1])
    return cart
    

if __name__ == '__main__':
    # userData = createUser()
    # with open("db/data/UsersGenerated.csv", "w+") as myCsv:
    #     csvWriter = csv.writer(myCsv, delimiter=',')
    #     csvWriter.writerows(userData)
    
    sellerData = createSeller()
    with open("db/data/SellerGenerated.csv", "w+") as myCsv:
        csvWriter = csv.writer(myCsv, delimiter=',')
        csvWriter.writerows(sellerData)

    productData = createProducts(sellerData)
    with open("db/data/ProductsGenerated.csv", "w+") as myCsv:
        csvWriter = csv.writer(myCsv, delimiter=',')
        csvWriter.writerows(productData)
    
    fundingData = createFunding()
    with open("db/data/FundingGenerated.csv", "w+") as myCsv:
        csvWriter = csv.writer(myCsv, delimiter=',')
        csvWriter.writerows(fundingData)

    purchasingData = createPurchases(fundingData, productData)
    with open("db/data/PurchasesGenerated.csv", "w+") as myCsv:
        csvWriter = csv.writer(myCsv, delimiter=',')
        csvWriter.writerows(purchasingData)
    
    cartData = createCart(productData)
    with open("db/data/CartGenerated.csv", "w+") as myCsv:
        csvWriter = csv.writer(myCsv, delimiter=',')
        csvWriter.writerows(cartData)
    
    