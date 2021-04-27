from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import logout
from app.models import *
from app.forms import *
from django.core.paginator import Paginator
from django.contrib.auth import views as auth_views

from django.http import HttpResponse


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
        data['page_obj'] = Paginator(Product.objects.all(), 9)

        page_number = request.GET.get('page')
        data['page_obj'] = data['page_obj'].get_page(page_number)

        if request.user.is_authenticated:
            if 'order' not in request.session:
                user_post = User.objects.get(username=request.user.username)
                clientprofile = Client.objects.get(user=user_post)

                x = Order.objects.create(client=clientprofile)

                request.session['order'] = x.pk

        if request.method == 'POST':
            return render(request, 'productsearch.html', data)

    return render(request, 'index.html', data)


# Dropdown selector that orders products by
def orderProductsBy(request, order_by):
    data = {}
    if request.method == 'GET':
        if order_by == "asc":
            data['products'] = Product.objects.all().order_by('price')
            data['page_obj'] = Paginator(data['products'], 9)

        else:
            data['products'] = Product.objects.all().order_by('price').reverse()
            data['page_obj'] = Paginator(data['products'], 9)

        categories = []
        for cat in Category.objects.all():
            categories.append(cat)
        data['categories'] = categories
        data['form'] = ProductQueryForm()

        page_number = request.GET.get('page')
        data['page_obj'] = data['page_obj'].get_page(page_number)

        return render(request, 'index.html', data)
    return redirect('index')


def byCategory(request, cat):
    data = {}
    if request.method == 'GET':
        data['form'] = ProductQueryForm()

        data['products'] = Product.objects.filter(category__name=cat)
        data['page_obj'] = Paginator(data['products'], 9)

        categories = []
        for cat in Category.objects.all():
            categories.append(cat)
        data['categories'] = categories

        page_number = request.GET.get('page')
        data['page_obj'] = data['page_obj'].get_page(page_number)

        return render(request, 'index.html', data)
    return redirect('index')


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
    Order.objects.filter(id=request.session['session']).delete()
    logout(request)
    return redirect('login')


def cart(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            order = Order.objects.get(pk=request.session['order'])

            total = sum([p.price for p in order.products.all()])

            data = {
                'products': order.products.all(),
                'total': total
            }

            return render(request, 'cart.html', data)

        return redirect('login')

    raise Http404


def addToCart(request, product_id, curr_url, curr_page=None):
    # if POST request, process form data
    print()
    if request.method == 'GET':
        if request.user.is_authenticated:
            product_to_add = Product.objects.get(pk=product_id)

            if product_to_add.quantity > 0:
                product_to_add.quantity = product_to_add.quantity - 1
                product_to_add.save()
            else:

                return HttpResponse("não dá para remover mais produtos")

            user_post = User.objects.get(username=request.user.username)
            clientprofile = Client.objects.get(user=user_post)

            order = Order.objects.get(pk=request.session['order'])

            order.products.add(product_to_add)
            order.save()

            caller = curr_url.replace("%2F", "/")

            if curr_page:
                url = caller + '?page=' + str(curr_page)
                return redirect(url)
            else:
                return redirect('index')

        else:
            return redirect('login')

    raise Http404


def cleanCart(request):
    Order.objects.get(pk=request.session['order']).products.clear()
    return redirect('cart')
