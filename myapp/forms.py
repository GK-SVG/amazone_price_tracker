from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email","password"]
        widgets = {
            'email':forms.EmailInput(attrs={'class':"form-control"}),
            'password':forms.PasswordInput(attrs={'class':"form-control"})
        }
        labels = {
            'email':"Email",
            'password':"Password"
        }
        