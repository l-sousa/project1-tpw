"""webproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/django', admin.site.urls),
    path('', views.indexView, name='index'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='account_logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('createaccount/', views.createAccountView, name='create account'),
    path('shopsearch/item/<int:pid>/', views.productDetailsView, name='product details'),
    path('shopsearch/', views.shopSearchView, name='shop search'),
    path('order_by/<str:order_by>/', views.orderProductsBy, name='order products by'),
    path('by_category/<str:cat>/', views.byCategory, name='select category'),
    path('cart/', views.cart, name='cart'),
    re_path(r'add_to_cart/(?P<product_id>[0-9]+)/(?P<curr_url>[^/]+)/(?P<curr_page>[0-9]+)?/$', views.addToCart,
            name='add to cart'),
    path('cart/clean/', views.cleanCart, name='clean cart'),
    path('cart/buy', views.buyCart, name='buy cart'),
    path('account/', views.clientAccountDetailsView, name='client account details'),
    path('account/myorders/', views.clientPastOrdersView, name='client past orders'),
    path('account/myorders/clean-orders', views.cleanOrders, name='clean past orders'),
    path('pagenotfound/', views.pageNotFoundView, name='page not found'),

    # ADMIN VIEWS
    path('admin/products/addproduct', views.adminAddNewProductView, name='admin add new product'),
    path('admin/products/', views.adminProductsView, name='admin edit products'),

]
