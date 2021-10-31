from faker import Faker
import csv
from werkzeug.security import generate_password_hash;
from random import seed
from random import randint

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
            user.append(f"{firstname}.{lastname}@{fake.domain_name()}")
            user.append(firstname)
            user.append(lastname)
            user.append(generate_password_hash(fake.word()))
            user.append(fake.street_address())
            user.append(None)
            user.append(fake.city())
            user.append(fake.state())
            user.append(fake.postcode())
            users.append(user)
            i +=1
    return users

def createSeller():
    sellers = []
    seed(1)
    while len(sellers) < 100:
        value = randint(0, 1000)
        if value not in sellers:
            sellers.append([value])
    return sellers

if __name__ == '__main__':
    userData = createUser()
    with open("db/data/UsersGenerated.csv", "w+") as myCsv:
        csvWriter = csv.writer(myCsv, delimiter=',')
        csvWriter.writerows(userData)

    sellerData = createSeller()
    with open("db/data/SellerGenerated.csv", "w+") as myCsv:
        csvWriter = csv.writer(myCsv, delimiter=',')
        csvWriter.writerows(sellerData)