from django.urls import path
from .views import index,login,signup,forget_password,verify_otp,logout

urlpatterns = [
    path('',index,name="Index"),
    path('login/',login,name="Login"),
    path('logout/',logout,name="Logout"),
    path('signup/',signup,name="Signup"),
    path('verify_otp/<str:mail>/',verify_otp,name="Otp"),
    path('forget_password/',forget_password,name="Forget_Password")
]
