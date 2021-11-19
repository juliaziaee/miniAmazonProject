import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://www.walmart.com/shop/deals'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
x = soup.findAll('div')


print(x)