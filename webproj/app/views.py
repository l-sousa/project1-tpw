from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect

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

#Search Items
def shopSearchView(request):
    data = {}

    # if POST request, process form data
    if request.method == 'POST':
        # create form instance and pass data to it
        form = ProductQueryForm(request.POST)
        if form.is_valid():  # is it valid?
            query = form.cleaned_data['query_prodname']
            pobj = Product.objects.filter(name__icontains=query)
            bobj = Product.objects.filter(brand__name__icontains=query)
            products = list(list(pobj) + list(bobj))
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


"""
    EXCLUSIVE ADMIN VIEWS 
"""

# Add a new product to the shop
def adminAddNewProductView(request):
    # Only if we're dealing with an admin!!
    if request.user.is_authenticated and request.user.is_superuser:
        data = {}
        if request.method == "POST":
            form = NewProductForm(request.POST)
            if form.is_valid():
                form.save()
                # newprod_name = form.cleaned_data['name']
                data['success'] = 'Novo produto adicionado com sucesso!'
                data['form'] = NewProductForm()
            # if GET (or any other method), create blank form
        else:
            form = NewProductForm()
            data['form'] = form
        return render(request, 'addproduct.html', data)
    else:
        return redirect('user404')

#Display all products in store + ability to edit their info
def adminProductsView(request):
    # Only if we're dealing with an admin!!
    if request.user.is_authenticated and request.user.is_superuser:
        data = {}
        # The admin wishes to edit a product
        if request.method == "POST":
            form = EditProductForm(request.POST)
            #print("POST AQUI")
            if form.is_valid():
                product = Product.objects.filter(id=form.cleaned_data['product_id'])[0]
                product.name = form.cleaned_data['name']
                product.description = form.cleaned_data['description']
                category_name = form.cleaned_data['category']
                category = Category.objects.filter(name=category_name)
                for c in category:
                    product.category.add(c.id)
                brand_name = form.cleaned_data['brand']
                brand = Brand.objects.filter(name=brand_name)
                for b in brand:
                    product.brand = b
                product.price = form.cleaned_data['price']
                product.quantity = form.cleaned_data['quantity']
                product.image = form.cleaned_data['image']
                product.save()
                data['success'] = 'Produto ' + product.name + ' editado com sucesso!'
                data['form'] = EditProductForm()
        # If GET, create blank form; pass products and categories
        else:
            form = EditProductForm()
        data['form'] = form
        products = Product.objects.all()
        data['products'] = list(products)
        categories = []
        for cat in Category.objects.all():
            categories.append(cat)
        data['all_cats'] = categories
        return render(request, 'viewproducts.html', data)
    else:
        return redirect('user404')