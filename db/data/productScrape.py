import requests
import urllib.request
from bs4 import BeautifulSoup
import csv

# https://www.blog.datahut.co/post/scrape-product-information-from-walmart-using-python-beautifulsoup

# url = 'https://www.walmart.com/shop/deals'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
# x = soup.findAll('div', {'class':'mb1 ph1 pa0-xl bb b--near-white w-25'})

# for i in range(len(x)):
#     productname = x[i].find('span', {'class': 'f6 f5-l normal dark-gray mb0 mt1 lh-title'})
#     if productname:
#         print(productname.text)
    
urls = ['https://www.aliceandolivia.com/womens-clothing/dresses/mini-dresses/?c=US', 'https://www.aliceandolivia.com/womens-clothing/dresses/midi-dresses/?c=US',
        'https://www.aliceandolivia.com/womens-clothing/tops-sweaters/blouses/?c=US', 'https://www.aliceandolivia.com/womens-clothing/womens-pants/?c=US']
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
        clothes.append([name.lower(),"{:.2f}".format(float(price)),image])
print(clothes)
print(len(clothes))

with open("db/data/clothes.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(clothes)