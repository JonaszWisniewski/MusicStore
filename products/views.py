from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewProductForm, EditProductForm
from .models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'products/product_detail.html', 
                  {'product': product,
                   'related_products': related_products})

@login_required
def new_product(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES) # information and files that user uploads

        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            

            return redirect('products:detail', pk=product.id)
    else:
        form = NewProductForm()

    return render(request, 'products/form.html', {
        'form': form,
        'title': 'Add New Product'
    })


@login_required
def delete_product(request, pk):
    # user = request.user
    
    product = get_object_or_404(Product, pk=pk)

    if product.created_by == request.user or request.user.is_staff:
   
        product.delete()

    return redirect('/')


@login_required
def edit_product(request, pk):
    
    product = get_object_or_404(Product, pk=pk)
    if product.created_by == request.user or request.user.is_staff: # user can delete his own products unless its a staff (admin person)
        if request.method == 'POST':
            form = EditProductForm(request.POST, request.FILES, instance=product) # information and files that user uploads

            if form.is_valid():
                product.save()
                messages.success(request, ("Product edited successfully"))

                return redirect('products:detail', pk=product.id)
        else:
            form = EditProductForm(instance=product)

        return render(request, 'products/form.html', {
            'form': form,
            'title': 'Edit Product'
        })
    else:
        return redirect('products:detail', pk=product.id)
        

