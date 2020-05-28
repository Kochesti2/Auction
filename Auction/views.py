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
    if request.user.is_authenticated:
        tri = three_recommended_items(request)
        if tri == 0:
            tri = []
        context = {'products':products, "tri":tri }

    return render(request,"home/home.html",context)


def about_view(request):
    my_context ={
        "my_text":"this is about us",
        "my_number":123,
        "my_list":[1,2,3,4,"abc"]
    }
    return render(request,"about.html",my_context)


def three_recommended_items(request):
    all_products = Product.objects.filter(disponible=True)
    user_products = Product.objects.filter(user__email=request.user.email)
    all_products = all_products.difference(user_products)

    all_products_names = []
    for p in all_products:
        all_products_names.append(p.name)


    user_products_names = []
    for p in user_products:
        user_products_names.append(p.name)

    if len(all_products_names) < 3 or len(user_products_names) < 1:
        return 0

    import textdistance
    # set test
    list = [[user_products_names[0], all_products_names[0], round(textdistance.jaro_winkler(user_products_names[0], all_products_names[0]), 4)],
            [user_products_names[0], all_products_names[1], round(textdistance.jaro_winkler(user_products_names[0], all_products_names[0]), 4)],
            [user_products_names[0], all_products_names[2], round(textdistance.jaro_winkler(user_products_names[0], all_products_names[0]), 4)]]

    # Jaro–Winkler distance is a measure of edit distance which gives more similar measures to words in which
    # the beginning characters match.

    for i in all_products_names:
        for j in user_products_names:
            d = round(textdistance.jaro_winkler(i, j), 4)
            m = min([t[2] for t in list])
            if d > m:
                l = [j,i, d]
                for k in range(3):
                    if m == list[k][2]:
                        list[k] = l
                        break

    from django.db.models import Q
    list = Product.objects.filter(Q(name = list[0][1]) | Q(name = list[1][1]) | Q(name = list[2][1]), disponible=True )
    return list

