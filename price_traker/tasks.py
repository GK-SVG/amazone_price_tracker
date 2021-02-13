from celery import shared_task 
from .models import Price_Tracker_Model
import requests
from bs4 import BeautifulSoup



header = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
            "Accept-Language":'en'
         }

@shared_task
def update_product_price():
    products = Price_Tracker_Model.objects.all()
    for product in products:
        product_url = product.amazone_product_url
        response = requests.get(product_url,headers=header)
        data = response.text
        soup = BeautifulSoup(data, features='html.parser')
        price = float(soup.find("span",{"id": "priceblock_ourprice"}).text[2:].replace(",",''))
        product.amazone_product_price = price
        print('price---',price)
        product.save()
