from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect

from app.models import *

# Create your views here.

def indexView(request):
    data = {}

    if request.method == 'GET':
        categories = []
        for cat in Category.objects.all():
            categories.append(cat)
        data['categories'] = categories

    return render(request, 'index.html', data)

