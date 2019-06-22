from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Products
from django.utils import timezone

def home(request):
    products = Products.objects
    return render(request, 'products/home.html', {'products':products})

@login_required(login_url='/accounts/signup')
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            products = Products()
            products.title=request.POST['title']
            products.body = request.POST['body']
            if request.POST['url'].startswith('https://') or request.POST['url'].startswith('http://'):
                products.url = request.POST['url']
            else:
                products.url = 'http://'+request.POST['url']
            products.icon = request.FILES['icon']
            products.image = request.FILES['image']
            products.pub_date = timezone.datetime.now()
            products.hunter = request.user
            products.save()
            return redirect('/products/' + str(products.id))
        else:
            return render(request, 'products/create.html', {'error': 'All field must be filled.'})
    return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    return render(request, 'products/detail.html', {'product':product})

@login_required(login_url='/accounts/signup')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/'+ str(product.id))