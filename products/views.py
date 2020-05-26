from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
from products.forms import Increment_price_form
from products.models import Product


def product_detail_view(request, **kwargs):
    pk  = kwargs['id']
    product = get_object_or_404(Product, pk=pk)
    form = Increment_price_form(request.POST or None)
    product.user
    if len(product.winner) > 0:
        s_name = request.user.first_name
        s_last = request.user.last_name
        winner_to_display = s_name[:3] + "**** ****" + s_last[len(s_last) - 3:len(s_last)]
    else:
        winner_to_display = "Be the first!"

    if form.is_valid():
        newPrice = form.cleaned_data.get("final_price")

        if newPrice > product.final_price + product.min_increment and form.is_valid():
            product.final_price = newPrice
            product.winner = str(request.user)
            product.user.add(request.user)
            product.save()

            s_name = request.user.first_name
            s_last = request.user.last_name
            winner_to_display = s_name[:3] + "**** ****" + s_last[len(s_last)-3:len(s_last)]
        else:
            messages.error(request, "Please insert more than " + str(float(product.final_price + product.min_increment)) + " €")

    context = {'object': product,'form':form,'winner_to_diplay':winner_to_display}
    return render(request, 'products/productPage.html', context)

def product_view(request):
    product = Product.objects.all()
    return render(request, '')

