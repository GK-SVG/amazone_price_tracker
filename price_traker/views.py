from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.

def price_tracker_home():
    url = "https://www.amazon.in/Realme-Buds-Android-Smartphones-Black/dp/B07XMFDHSG/ref=sr_1_1?dchild=1&keywords=realme&qid=1612885307&s=electronics&sr=1-1"
    response = requests.get(url)
    data = response.text
    # print("---------------------------data-------------------------------")
    # print(data)
    soup = BeautifulSoup(data, features='html.parser')
    print("---------------------------Soup-------------------------------")
    # print(soup)
    img_div = soup.find("div", {"id": "imgTagWrapperId"})
    print(img_div)


price_tracker_home()