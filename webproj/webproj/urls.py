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
from django.urls import path
from django.contrib.auth import views as auth_views

from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexView, name='index'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='account_logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('createaccount/', views.createAccountView, name='create account'),
    path('item/<int:pid>/', views.productDetailsView, name='product details'),
    path('shopsearch/', views.shopSearchView, name='shop search'),

    path('order_by/<str:order_by>/', views.orderProductsBy, name='order products by'),
    path('by_category/<str:cat>/', views.byCategory, name='select category'),
    path('range_slider/', views.rangeSlider, name='range slider'),

]
