from django.urls import path
from .views import post_product,price_tracker_home

urlpatterns = [
    path("post_product/",post_product,name="Post_product"),
    path("",price_tracker_home,name="Price_Tracker_Home")
]
