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
                                     widget=forms.TextInput(attrs={'placeholder': 'O que procura?'}))


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