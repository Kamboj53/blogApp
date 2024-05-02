from django import forms
from .models import *

class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 50,label = "Enter your username")
    password = forms.CharField(max_length=20,label = "Enter your password",widget = forms.PasswordInput)
    confirm_password = forms.CharField(max_length=20,label ="Confirm your password",widget = forms.PasswordInput)
    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm_passsword = self.cleaned_data.get("confirm_password")

        if password and confirm_passsword and password != confirm_passsword:
            raise forms.ValidationError("Password Don't Match")

        values = {
            "username" : username,
            "password" : password
        }
        return values
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Enter your username')
    password = forms.CharField(max_length=20,label = "Enter your password",widget = forms.PasswordInput)
    
    
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = '__all__' 
