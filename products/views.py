from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
# Create your views here.
from products.forms import Increment_price_form
from products.models import Product
from users.admin import User


def product_detail_view(request, **kwargs):
    pk  = kwargs['id']
    product = get_object_or_404(Product, pk=pk)
    form = Increment_price_form(request.POST or None)
    increment = product.min_increment+product.final_price
    product.user
    try:
        if len(product.winner) > 0:
            u = User.objects.filter(email=product.winner)
            s_name = u.first().first_name
            s_last = u.first().last_name
            winner_to_display = s_name[:3] + "**** ****" + s_last[len(s_last) - 3:len(s_last)]
        else:
            winner_to_display = "Be the first!"
    except:
        winner_to_display = "Be the first!"

    if request.method == 'POST' and request.user.is_anonymous == True:
        messages.error(request,"Please register!")
        return redirect('create')


    if form.is_valid():
        newPrice = form.cleaned_data.get("final_price")

        if newPrice > product.final_price + product.min_increment and form.is_valid():
            product.final_price = newPrice
            product.winner = str(request.user)
            product.user.add(request.user)
            increment = product.min_increment + product.final_price
            product.save()

            u = User.objects.filter(email=product.winner)
            s_name = u.first().first_name
            s_last = u.first().last_name
            winner_to_display = s_name[:3] + "**** ****" + s_last[len(s_last)-3:len(s_last)]
        else:
            messages.error(request, "Please insert more than " + str(float(product.final_price + product.min_increment)) + " €")

    context = {'object': product,'form':form,'winner_to_diplay':winner_to_display,'increment':increment}
    return render(request, 'products/productPage.html', context)



def search_view(request):
    if request.method == 'POST':
        query= request.POST.get('q')
        if query != "":
            print(query)
            products = Product.objects.filter(name__contains=query)
            products = products.union(Product.objects.filter(description__contains=query))
            context = {'products': products}
            return render(request, 'products/search.html', context)

    return redirect('home')








