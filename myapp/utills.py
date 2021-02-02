import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import Code
from django.contrib.auth.models import User


username="gkdevtest777@gmail.com"
password="gk138028"


def send_mail(from_email="gkdevtest777@gmail.com",subject="Mail Verification",to_email=None):
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] =to_email
    msg['Subject'] = subject
    user = User.objects.get(email=to_email)
    if not Code.objects.filter(user=user).exists():
        code = Code(user=user)
        code.save()
    else:
        code = Code.objects.get(user=user)
        code.delete()
        code = Code(user=user)
        code.save()
    html = f"<h1>Your OTP is {code.code}</h1>"
    html_part = MIMEText(html,"html")
    msg.attach(html_part)
    msg_str = msg.as_string()
    server =smtplib.SMTP(host="smtp.gmail.com",port=587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    try:
        server.sendmail(from_email,to_email,msg_str)
        server.quit()
        return True
    except:
        server.quit()
        return False
    
    
       



