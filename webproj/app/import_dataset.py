import csv

import django
django.setup()

from django.conf import settings
settings.configure()



from app.models import Category, Brand, Product



with open('/../dataset/categories.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Brand.objects.get_or_create(
            name=row[0]
        )


'''with open('/../dataset/brands.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Brand.objects.get_or_create(
            name=row[0],
        )'''
