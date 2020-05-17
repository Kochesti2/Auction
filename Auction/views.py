from django.http import HttpResponse
from django.shortcuts import render
from users.models import Product

def homeView(request):
    # if request.user.is_authenticated:
    #     context = {'auth':True}
    #     authed = True
    # else:
    #     context = {'auth':False}
    #     authed = False

    products = Product.objects.all()

    context = {'products':products }
    return render(request,"home/home.html",context)


def about_view(request):
    my_context ={
        "my_text":"this is about us",
        "my_number":123,
        "my_list":[1,2,3,4,"abc"]
    }
    return render(request,"about.html",my_context)

