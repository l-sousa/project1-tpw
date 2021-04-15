import csv

import django
import json
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webproj.settings')

django.setup()

from django.conf import settings

settings.configure()

from models import Category, Brand, Product

# with open('/../dataset/categories.csv') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         _, created = Brand.objects.get_or_create(
#             name=row[0]
#         )

# with open('/../dataset/brands.csv') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         _, created = Brand.objects.get_or_create(
#             name=row[0],
#         )

with open('../dataset/products.json') as f:
    data = json.load(f)
    for p in data:
        print(p)


