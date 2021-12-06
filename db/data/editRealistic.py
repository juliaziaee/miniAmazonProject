import csv
import random

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