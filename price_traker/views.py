from django.shortcuts import render,redirect,HttpResponse
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from .models import Price_Tracker_Model
from django.contrib import messages


# Create your views here.
header = {
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
            "Accept-Language":'en'
         }


@login_required(login_url="Login")
def post_product(request):
    if request.method=="POST":
        product_url = request.POST.get("url","")
        my_desired_price = request.POST.get("price","")
        response = requests.get(product_url,headers=header)
        data = response.text
        soup = BeautifulSoup(data, features='html.parser')
        title = soup.find("h1",{"id": "title"}).text.strip("\n")
        img_url   = soup.find("img",{"class": "a-dynamic-image"}).get("data-old-hires")
        price = float(soup.find("span",{"id": "priceblock_ourprice"}).text[2:].replace(",",''))
        product = Price_Tracker_Model(user=request.user,amazone_product_url=product_url,amazone_product_title=title,amazone_product_price=price,my_price=float(my_desired_price),product_img=img_url)
        product.save()
        messages.success(request,"Product Addded Successfully")
        return redirect("Price_Tracker_Home")

    
    
@login_required(login_url="Login")
def price_tracker_home(request):
    my_products = Price_Tracker_Model.objects.filter(user=request.user)
    return render(request,"price_traker/home.html",{"my_products":my_products})