from django import forms
from app.models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm


class CreateAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional')
    email = forms.EmailField(max_length=200, help_text='Please inform a valid email address')
    address = forms.CharField(max_length=200, required=True, help_text='Please inform a email address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'address', 'password1', 'password2',)


class ProductQueryForm(forms.Form):
    query_prodname = forms.CharField(label='Search:', max_length=100,
                                     widget=forms.TextInput(attrs={'placeholder': 'O que procura?',
                                                                   'class': 'search_bar_products mr-sm-2'}))


class RangeSliderForm(forms.Form):
    min_value = forms.CharField(widget=forms.TextInput(attrs={'id': 'minamount'}))
    max_value = forms.IntegerField(widget=forms.TextInput(attrs={'id': 'maxamount'}))


class AccountDetailsUpdateForm(UserChangeForm):
    first_name = forms.CharField(max_length=50, required=False, help_text='Optional', label='Primeiro Nome')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional', label='Último Nome')
    email = forms.EmailField(max_length=200, help_text='Required. Please inform a valid email address', label='Endereço de Email')
    address = forms.CharField(max_length=200, required=False, help_text='Optional', label='Morada')
    username = forms.CharField(max_length=25, label='Username')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'address')

class AccountPasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=30, label='Password Atual')
    new_password1 = forms.CharField(max_length=30, label='Nova Password')
    new_password2 = forms.CharField(max_length=30, label='Confirmação da Nova Password')

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


"""
    ADMIN FORMS
"""

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'brand', 'price', 'quantity']

class EditProductForm(forms.Form):
    product_id = forms.IntegerField()
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=150)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False)
    price = forms.DecimalField(max_digits=5, decimal_places=2)
    quantity = forms.DecimalField(max_digits=3, decimal_places=0)
    image = forms.URLField()