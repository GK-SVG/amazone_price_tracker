from django.shortcuts import render,HttpResponse
from .forms import UserForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="Login")
def index(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        return HttpResponse("form submitted")
    return render(request,"base.html",{'form':form})


def login(request):
    if request.method == "POST":
        pass
    form = UserForm()
    return render(request,'User/Login.html',{'form':form})


def signup(request):
    if request.method=="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            pass
    form = UserForm()
    return render(request,"User/Signup.html",{'form':form})


def forget_password(request):
    return render(request,'User/forgetPassword.html')