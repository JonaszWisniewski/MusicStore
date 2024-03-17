from django.views.generic import ListView
from django.shortcuts import render

from products.models import Category, Product

from django.core.paginator import Paginator

def index(request):
    products = Product.objects.filter(is_sold=False)

    categories = Category.objects.all()

    page = Paginator(products, 2)

    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    return render(request, 'store/index.html', {'categories': categories,
                                                'page': page,
                                                })



def contact(request):
    return render(request, 'store/contact.html')



