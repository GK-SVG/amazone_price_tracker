from django import forms
from django.contrib.auth.models import User
from .models import Links

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

class LinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = Links
        fields = ["title","url","tags","public"]

        widgets = {
            'title':forms.TextInput(attrs={'class':"form-control my-2 w-100 col-sm-11 col-md-11 col-12",'placeholder': 'Enter Title here'}),
            'url':forms.URLInput(attrs={'class':"form-control my-2 w-100 col-sm-11 col-md-11 col-12",'placeholder': 'Enter valid URL'}),
            'tags':forms.TextInput(attrs={'class':"form-control my-2 w-100 col-sm-11 col-md-11 col-12",'placeholder': 'Enter tags with Start of #'}),
            'public':forms.CheckboxInput(attrs={'class':"mt-3 myCheckbox col-sm-1 col-md-1 col-12",'checked':'checked'})
        }
        required = ("title","url","tags","public")
                    
       