from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def homeView(request):
    # if request.user.is_authenticated:
    #     context = {'auth':True}
    #     authed = True
    # else:
    #     context = {'auth':False}
    #     authed = False

    products_list = Product.objects.all().order_by("id")
    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {'products':products }
    return render(request,"home/home.html",context)


def about_view(request):
    my_context ={
        "my_text":"this is about us",
        "my_number":123,
        "my_list":[1,2,3,4,"abc"]
    }
    return render(request,"about.html",my_context)

