from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
from users.models import Product


def product_detail_view(request, **kwargs):
    pk  = kwargs['id']
    product = get_object_or_404(Product, pk=pk)
    context = {'object': product}
    return render(request, 'products/productPage.html', context)