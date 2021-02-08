from django.urls import path
from .views import (login,signup,forget_password,
                    verify_otp,logout,reset_password,mylink,post_link,delete_link)

urlpatterns = [
    path('login/',login,name="Login"),
    path('logout/',logout,name="Logout"),
    path('signup/',signup,name="Signup"),
    path('verify_otp/<str:mail>/',verify_otp,name="Otp"),
    path('forget_password/',forget_password,name="Forget_Password"),
    path('reset_password/<str:mail>/',reset_password,name="Reset_Password"),
    path('',mylink,name="MyLink"),
    path('post_link/',post_link,name="Post_Link"),
    path('delete_link/<int:id>',delete_link,name="Delete_Link")
]
