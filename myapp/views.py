from django.shortcuts import render,HttpResponse,redirect
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from .utills import send_mail
from django.contrib.auth.models import User
from .models import Code,MailValid
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
            mail = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2=request.POST.get('password2')
            if not(User.objects.filter(email=mail).exists()):
                if password2==password:
                    try:
                        username = mail
                        user = User(username=username,email=mail,password=password)
                        user.save()
                        send_mail(to_email=mail)
                        MailValid(user=user).save()
                        return redirect('Otp',mail)
                    except:
                        return HttpResponse('Something went wrong')
                else:
                    return HttpResponse("Password do not match")
            else:
                return HttpResponse("Email Already taken")
    form = UserForm()
    return render(request,"User/Signup.html",{'form':form})


def verify_otp(request,mail):
    if request.method=="POST":
        print(request.POST)
        otp = request.POST.get('otp')
        if User.objects.filter(email=mail).exists():
            user = User.objects.get(email=mail)
            otp = Code.objects.get(user=user)
            print('otp--',otp.code)
            print('user--',user)
            if otp.code==str(otp):
                mailvalidate = MailValid.objects.get(user=user)
                mailvalidate.mail_valid = True
                mailvalidate.save()
                otp.delete()
                return render(request,"base.html")
    return render(request,"User/otp.html")

def forget_password(request):
    return render(request,'User/forgetPassword.html')