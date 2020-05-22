from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
from products.forms import Increment_price_form
from products.models import Product


def product_detail_view(request, **kwargs):
    pk  = kwargs['id']
    product = get_object_or_404(Product, pk=pk)
    form = Increment_price_form(request.POST or None)
    context = {'object': product,'form':form}
    product.user
    if form.is_valid():
        newPrice = form.cleaned_data.get("final_price")

        if newPrice > product.final_price + product.min_increment and form.is_valid():
            product.final_price = newPrice
            product.winner = str(request.user)
            product.user.add(request.user)
            product.save()


    return render(request, 'products/productPage.html', context)

def product_view(request):
    product = Product.objects.all()
    return render(request, '')
