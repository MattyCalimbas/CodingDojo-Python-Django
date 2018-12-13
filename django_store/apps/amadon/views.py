from django.shortcuts  import render, HttpResponse, redirect
from . models import *

def index(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'index.html', context)

def buy(request):
    if 'count' not in request.session:
        request.session['count'] = 0
    if 'total' not in request.session:
        request.session['total'] = 0
    if request.POST['product'] == '1':
        request.session['total'] += float(request.POST['quantity']) * 19.99
    if request.POST['product'] == '2':
        request.session['total'] += float(request.POST['quantity']) * 29.99
    if request.POST['product'] == '3':
        request.session['total'] += float(request.POST['quantity']) * 4.99
    if request.POST['product'] == '4':
        request.session['total'] += float(request.POST['quantity']) * 49.99
    request.session['count'] += int(request.POST['quantity'])
    return redirect ('/checkout')


def checkout(request):
    return render(request, 'checkout.html')