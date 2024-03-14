from django.views.generic import ListView
from django.shortcuts import render

from products.models import Category, Product

from django.core.paginator import Paginator

class ProductListView(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'post'
    paginate_by = 2

def index(request):
    products = Product.objects.filter(is_sold=False)

    categories = Category.objects.all()

    return render(request, 'store/index.html', {'categories': categories,
                                                'products': products,
                                                })



def contact(request):
    return render(request, 'store/contact.html')



