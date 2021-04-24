from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import logout
from app.models import *
from app.forms import *


# Create your views here.

def indexView(request):
    data = {}
    if request.method == 'GET':
        categories = []
        for cat in Category.objects.all():
            categories.append(cat)
        searchform = ProductQueryForm()
        data['categories'] = categories
        data['form'] = searchform
        data['products'] = list(Product.objects.all())
        data['products_length'] = range(len(data['products']))
    if request.method == 'POST':
        return render(request, 'productsearch.html', data)

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


# Product Details
def productDetailsView(request, pid):
    data = {}
    product = Product.objects.get(id=pid)

    # cli = Client.objects.get(user_id=request.user.id) #Get the user id
    if request.method == 'POST':
        # process buy
        return print("oki")
    else:
        data['product'] = product
        # data['client'] = cli
        return render(request, 'productdetails.html', data)


# Search Items
def shopSearchView(request):
    data = {}
    print("######################################################")

    # if POST request, process form data
    if request.method == 'POST':
        # create form instance and pass data to it
        form = ProductQueryForm(request.POST)
        if form.is_valid():  # is it valid?
            query = form.cleaned_data['query_prodname']
            pobj = Product.objects.filter(name__icontains=query)
            bobj = Product.objects.filter(brand__name__icontains=query)
            products = list(set(list(list(pobj) + list(bobj))))
            data['products'] = products

            categories = []
            for cat in Category.objects.all():
                categories.append(cat)
            data['all_cats'] = categories
            data['query_prodname'] = query
            form = ProductQueryForm()
            data['form'] = form

            return render(request, 'productsearch.html', data)

    # if GET (or any other method), create blank form
    else:
        form = ProductQueryForm()
        data['form'] = form
    return render(request, 'index.html', data)


def account_logout(request):
    logout(request)
    return redirect('login')
