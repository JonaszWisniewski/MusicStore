from django.shortcuts import render

from products.models import Category, Product

def index(request):
    products = Product.objects.filter(is_sold=False)
    categories = Category.objects.all()
    return render(request, 'store/index.html', {'categories': categories,
                                                'products': products,
                                                })

def contact(request):
    return render(request, 'store/contact.html')



