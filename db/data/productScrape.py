import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# https://www.blog.datahut.co/post/scrape-product-information-from-walmart-using-python-beautifulsoup

url = 'https://www.walmart.com/shop/deals'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
x = soup.findAll('div', {'class':'mb1 ph1 pa0-xl bb b--near-white w-25'})

for i in range(len(x)):
    productname = x[i].find('span', {'class': 'f6 f5-l normal dark-gray mb0 mt1 lh-title'})
    if productname:
        print(productname.text)