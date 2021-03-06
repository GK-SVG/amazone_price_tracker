from django.shortcuts import render,HttpResponse,redirect
from .forms import UserForm,LinkForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .utills import send_mail
from django.contrib.auth.models import User
from .models import Code,MailValid,Links
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
# Create your views here.


def login(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        username = request.POST.get("email",'')
        password = request.POST.get("password",'')
        try:
            user = User.objects.get(username=username,password=password)
            auth.login(request,user)
            messages.success(request,"User Logged In Successfully")
            return redirect('MyLink')
        except:
            messages.warning(request,"Invalid Username or Password")
    form = UserForm()
    return render(request,'User/Login.html',{'form':form})


def signup(request):
    if request.method=="POST":
        print(request.POST)
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
                        messages.success(request,"Check your registered Mail for OTP")
                        return redirect('Otp',mail)
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
        otp = request.POST.get('otp')
        if User.objects.filter(email=mail).exists():
            user = User.objects.get(email=mail)
            otp = Code.objects.get(user=user)
            if otp.code==str(otp):
                mailvalidate = MailValid.objects.get(user=user)
                mailvalidate.mail_valid = True
                mailvalidate.save()
                otp.delete()
                return redirect("Login")
            else:
                messages.warning(request,"Entered OTP is Invalid")
    return render(request,"User/otp.html")


def forget_password(request):
    if request.method == "POST":
        print(request.POST)
        email = request.POST.get('email',None)
        if email:
            if User.objects.filter(email=email).exists():
                send_mail(to_email=email)
                messages.success(request,"Check your registered Mail for OTP")
                return render(request,'User/otp.html',{'email':email})
        otp = request.POST.get('otp',None)
        if otp:
            email = request.POST.get('otp_email')
            user = User.objects.get(email=email)
            otp = Code.objects.get(user=user)
            if otp.code==str(otp):
                otp.delete()
                messages.success(request,"OTP Veified Reset Password")
                return redirect("Reset_Password",email)
            messages.warning(request,"Invalid OTP")
    return render(request,'User/forgetPassword.html')


def reset_password(request,mail):
    if request.method=="POST":
        password = request.POST.get("password")
        password2 = request.POST.get("confirm-password")
        if password == password2:
            try:
                user = User.objects.get(username=mail)
                user.password = password
                user.save()
                messages.success(request,"Password Updated Successfully")
                return redirect("Login")
            except:
                messages.warning(request,"Something Went Wrong")
                return render(request,"User/reset_password.html")
        messages.warning(request,"Password Do not match")
    return render(request,"User/reset_password.html")
    

def logout(request):
    auth.logout(request)
    messages.success(request,"User Logout Successfully")
    return redirect("Index")


@login_required(login_url="Login")
def mylink(request):
    user = request.user           
    form = LinkForm()
    return render(request,"myapp/mylink.html",{'form':form})


@login_required(login_url="Login")
def post_link(request):
    user = request.user
    if request.is_ajax and request.method=="POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            url = form.cleaned_data['url']
            instance = Links(user=user,title=title,url=url)
            instance.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)


@login_required(login_url="Login")
def delete_link(request,id):
    user = request.user
    if Links.objects.filter(user=user,id=id).exists():
        del_link = Links.objects.get(user=user,id=id)
        del_link.delete()
        messages.success(request,"Link Deleted Successfully")
        return redirect('MyLink')
    messages.error(request,"Action not Allowed")
    return redirect('MyLink')