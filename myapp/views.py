from django.shortcuts import render,HttpResponse,redirect
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .utills import send_mail
from django.contrib.auth.models import User
from .models import Code,MailValid
from django.contrib import messages
# Create your views here.

@login_required(login_url="Login")
def index(request):
    return render(request,"base.html")


def login(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        username = request.POST.get("email",'')
        password = request.POST.get("password",'')
        user = User.objects.get(username=username,password=password)
        auth.login(request,user)
        messages.success(request,"User Logged In Successfully")
        return redirect('Index')
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
                        valid_mail = send_mail(to_email=mail)
                        if valid_mail:
                            MailValid(user=user).save()
                            messages.success(request,"Check your registered Mail for OTP")
                            return redirect('Otp',mail)
                        else:
                            messages.warning(request,"Entered Mail is invalid")
                    except:
                        messages.warning(request,"Something went Wrong please check your mail is correct")
                else:
                    messages.warning(request,"Password do not match ")
            else:
                messages.warning(request,"User Already Exist")
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
                print('mailvalited',mailvalidate.mail_valid)
                otp.delete()
                return redirect("Login")
            else:
                messages.warning(request,"Entered OTP is Invalid")
    return render(request,"User/otp.html")

def forget_password(request):
    return render(request,'User/forgetPassword.html')


def logout(request):
    auth.logout(request)
    messages.success(request,"User Logout Successfully")
    return redirect("Login")