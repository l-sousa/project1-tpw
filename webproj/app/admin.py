from django.contrib import admin
from app.models import Client, Category, Brand, Order, Product

# Register your models here.
admin.site.register(Client)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(Product)