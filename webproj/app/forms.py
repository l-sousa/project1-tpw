from django import forms
from app.models import *
from django.contrib.auth.forms import UserCreationForm

class CreateAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional')
    email = forms.EmailField(max_length=200, help_text='Please inform a valid email address')
    address = forms.CharField(max_length=200, required=True, help_text='Please inform a valid email address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'address', 'password1', 'password2',)

class ProductQueryForm(forms.Form):
    query_prodname = forms.CharField(label='Search:', max_length=100,
                                     widget=forms.TextInput(attrs={'placeholder': 'O que procura?', 'class': 'search_bar_products mr-sm-2'}))


