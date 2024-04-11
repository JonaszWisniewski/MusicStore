from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import Q

from products.models import Category, Product

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    cat_id = request.GET.get('category_id')
    list_of_prods = Product.objects.filter(is_sold=False)
    query = request.GET.get('q') # gets the user input from the search
    if query: 
        list_of_prods = Product.objects.filter(
            Q(name__icontains=query) | Q(price__icontains=query) |
            Q(category__name__icontains=query))
        
    if cat_id:
        list_of_prods = Product.objects.filter(category=cat_id)

    categories = Category.objects.all()    
    paginator = Paginator(list_of_prods, 2) # 2 products per page
    page = request.GET.get('page')

    try:
        list_of_prods = paginator.page(page)
    except PageNotAnInteger:
        if list_of_prods:
            list_of_prods = paginator.page(1)
        
    except EmptyPage:
        list_of_prods = paginator.page(paginator.num_pages)
        

    return render(request, 'store/index.html', {'categories': categories,
                                                'list_of_prods': list_of_prods
                                                })

def contact(request):
    return render(request, "store/contact.html")



