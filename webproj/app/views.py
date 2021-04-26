from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash

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


def prefillForm(clientprofile):
    # Pre-fill the form with current data
    form = AccountDetailsUpdateForm()
    form.fields['first_name'].initial = clientprofile.user.first_name
    form.fields['last_name'].initial = clientprofile.user.last_name
    form.fields['email'].initial = clientprofile.user.email
    form.fields['address'].initial = clientprofile.address
    form.fields['username'].initial = clientprofile.user.username
    return form


def clientAccountDetailsView(request):
    # In order to edit, the user must be logged in
    if request.user.is_authenticated:
        data = {}
        # Fetch current user
        user_post = User.objects.get(username=request.user.username)
        clientprofile = Client.objects.get(user=user_post)
        # if POST request, process form data
        if request.method == 'POST':
            form_general = AccountDetailsUpdateForm(request.POST, instance=request.user)
            form_passwd = AccountPasswordUpdateForm(request.user, request.POST)
            # The user wished to update his password
            if 'old_password' in request.POST:
                # is it valid tho?
                if form_passwd.is_valid():
                    user = form_passwd.save()
                    update_session_auth_hash(request, user)
                    user.client = request.user
                    clientprofile = Client.objects.get(user_id=user.client.id)
                    user.save()
                    user.refresh_from_db()
                    # Pre-fill the form with current data -> Give it to the template
                    data['formgeneral'] = prefillForm(clientprofile)
                    data['formpasswd'] = form_passwd
                    data['success'] = 'Password alterada com sucesso!'
                    return render(request, 'accountdetails.html', data)
                else:
                    data['invalid'] = 'Erro na alteração da palavra-passe! Por favor, verifique.'
                    # Pre-fill the form with current data -> Give it to the template
                    data['formgeneral'] = prefillForm(clientprofile)
                    data['formpasswd'] = form_passwd
            # The user wished to update his general information
            else:
                # is it valid tho?
                if form_general.is_valid():
                    newinfo = form_general.save()
                    newinfo.client = request.user
                    clientprofile = Client.objects.get(user_id=newinfo.client.id)
                    newinfo.save()
                    newinfo.refresh_from_db()
                    # Pre-fill the form with current data -> Give it to the template
                    data['formgeneral'] = prefillForm(clientprofile)
                    data['formpasswd'] = form_passwd
                    data['success'] = 'Informações gerais alteradas com sucesso!'
                    return render(request, 'accountdetails.html', data)
                else:
                    data['invalid'] = 'Erro na alteração dos dados! Por favor, verifique.'
                    # Pre-fill the form with current data -> Give it to the template
                    data['formgeneral'] = prefillForm(clientprofile)
                    data['formpasswd'] = form_passwd
        # if GET (or any other method), create blank form (accessing the page 1st time)
        else:
            # Pre-fill the form with current data
            form = prefillForm(clientprofile)
            # Give it to the template
            data['formgeneral'] = form
            data['formpasswd'] = PasswordChangeForm(request.user)
        return render(request, 'accountdetails.html', data)
    else:
        # The user is not logged in, so we redirect to that page
        return redirect('login')


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
        return redirect('page not found')

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
                data['success'] = 'Produto "' + product.name + '" editado com sucesso!'
                data['form'] = EditProductForm()
            # Something went wrong
            else:
                #print("FODEU")
                data['invalid'] = 'Erro na edição de produto!'
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
        return redirect('page not found')

def pageNotFoundView(request):
    out = render(request, 'pagenotfound.html')
    out.status_code = 404
    return out