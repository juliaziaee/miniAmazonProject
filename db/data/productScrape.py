import requests
import urllib.request
from bs4 import BeautifulSoup
import csv

# URLs for products from Alice and Olivia
urls = ['https://www.aliceandolivia.com/womens-clothing/dresses/mini-dresses/?c=US', 'https://www.aliceandolivia.com/womens-clothing/dresses/midi-dresses/?c=US',
        'https://www.aliceandolivia.com/womens-clothing/tops-sweaters/blouses/?c=US', 'https://www.aliceandolivia.com/womens-clothing/womens-pants/?c=US']
# Create clothing items and append them to clothes
clothes = []
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    x = soup.findAll('div', {'class':'product bfx-price-product'})
    for i in x:
        name = i.find('img', {'class':'tile-image lazy-image front-card'}).get('alt')
        name = ' '.join(name.split("-")[0:-1])
        price = i.find('span', {'class':'value bfx-price bfx-list-price'}).get('content')
        image = i.find('img', {'class':'tile-image lazy-image front-card'}).get('data-lazy')
        # Gets real product name, price and image
        clothes.append([name.lower(),"{:.2f}".format(float(price)),image])
print(clothes)
print(len(clothes))

# Write scraped clothing data to a CSV
with open("db/data/clothes.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(clothes)