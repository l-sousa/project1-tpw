from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect

from app.models import *
from app.forms import *

# Create your views here.

def indexView(request):
    data = {}

    if request.method == 'GET' or request.method=='POST':
        categories = []
        for cat in Category.objects.all():
            categories.append(cat)
        data['categories'] = categories

    return render(request, 'index.html', data)

# Create new user account
def createAccountView(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            client = Client(user=new_user)
            client.save()
            new_user.refresh_from_db()
            return redirect('index')
    else:
        form = CreateAccountForm()
        return render(request, 'createaccount.html', {'form': form})

#Product Details
def productDetailsView(request, pid):
    data = {}
    product = Product.objects.get(id=pid)
    # Only see the product details if the user is logged in
    if request.user.is_authenticated:
        # cli = Client.objects.get(user_id=request.user.id) #Get the user id
        if request.method == 'POST':
            # process buy
            return print("oki")
        else:
            data['product'] = product
            # data['client'] = cli
            return render(request, 'productdetails.html', data)
    else:
        return redirect('index')




