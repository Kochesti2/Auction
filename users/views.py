from datetime import datetime
from django.contrib.auth import get_user_model, logout
from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone
from products.models import Product, ProductImage
from django.contrib.auth.decorators import login_required
from users.forms import RegisterForm, Profile_user_form, new_auction_form
from users.models import Profile

User = get_user_model()
def register_page(request):
    print(request.method)
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        print(form.cleaned_data)
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        tel  =form.cleaned_data.get("phone_number")
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        new_user = User.objects.create_user( email, first_name, last_name, password, tel)
        messages.success(request,"Thank you for registration, now you can log in!")
        return HttpResponseRedirect('/')

    return render(request, "registration/user_create.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def new_auction_page(request):

    extra = 4 if request.user.is_premium else 1
    ImageFormset = modelformset_factory(ProductImage, fields=('image',),extra=extra)
    form = new_auction_form(request.POST or None)
    formset = ImageFormset(request.POST or None, request.FILES or None)

    try:
        prof = Profile.objects.get(user=request.user)
    except:
        messages.warning(request, 'You have to provide your information before you start an auction')
        url = reverse('profileit')
        return redirect(url)
    NumeroProdottiPerCliente = Product.objects.filter(profile=prof).count()
    print(NumeroProdottiPerCliente)
    if NumeroProdottiPerCliente >= 3 and not request.user.premium:
        return render(request, "users/credit_card.html", {})


    if form.is_valid() or formset.is_valid():
        name  = form.cleaned_data.get("name")
        try:
            if len(name) > 40:
                messages.error(request, "Name is too long")
                return redirect('create-auction')
        except:
            messages.error(request, "Name is too long")
            return redirect('create-auction')

        description = form.cleaned_data.get("description")
        try:
            if len(description) > 300:
                messages.error(request, "Description is too long max 300 characters")
                return redirect('create-auction')
        except:
            messages.error(request, "Description is too long max 300 characters")
            return redirect('create-auction')

        price = form.cleaned_data.get("price")
        try:
            if price <= 0 or price > 50000000:
                messages.error(request, "Price should be between 0 - 50'000'000")
                return redirect('create-auction')
        except:
            messages.error(request, "Price should be between 0 - 50'000'000")
            return redirect('create-auction')

        min_increment = form.cleaned_data.get("min_increment")
        try:
            print(min_increment)
            if min_increment <= 0:
                messages.error(request, "Increment cannot be negative")
                return redirect('create-auction')
        except:
            messages.error(request, "Increment cannot be negative")
            return redirect('create-auction')

        end_date = form.cleaned_data.get("end_date")
        try:
            if form.cleaned_data.get("end_date") < datetime.date(timezone.localtime(timezone.now())):
                messages.error(request, "Date not valid!")
                return redirect('create-auction')
        except:
            messages.error(request, "Date not valid!")
            return redirect('create-auction')

        p = Product(name=name,description= description,price=price,min_increment=min_increment,end_date=end_date,final_price=price,profile = prof)
        p.save()

        for f in formset:
            try:
                print(f)
                photo = ProductImage(product = p, image=f.cleaned_data['image'])
                print(type(f.cleaned_data['image']))
                photo.save()
            except Exception as e:
                break
        if formset.total_form_count() == 0:
            print("non ci sono immagini")

        messages.success(request, 'You have successfully created a new auction!')
        return redirect('home')


    if request.method == 'GET':
        formset = ImageFormset(queryset=ProductImage.objects.none())
    context = {
        "form": form, "formset":formset
    }
    return render(request, "users/new_auction.html", context)

@login_required
def profile_change(request):
    print(request.method)

    try:
        usr = request.user
    except:
        raise Http404

    try:
        usr.profile
        form = Profile_user_form(request.POST or None,request.FILES )
    except:
        form = Profile_user_form(request.POST or None,request.FILES)

    if form.is_valid():
        country  = form.cleaned_data.get("country")
        city = form.cleaned_data.get("city")
        address = form.cleaned_data.get("address")
        zip_code = form.cleaned_data.get("zip_code")
        photo = form.cleaned_data.get("photo")


        p = Profile.objects.create_update_Profile(usr,country,city,address,zip_code,photo)
        messages.success(request, 'Profile successfully updated')
        return HttpResponseRedirect('/')
    else:
        form = Profile_user_form()

    context = {
        "form": form,
    }
    return render(request, "users/profile_page.html", context)

@login_required
def get_premium(request):
    return render(request, "users/credit_card.html", {})

@login_required
def get_premium_after(request):
    try:
        usr = User.objects.get(id=request.user.id)
    except:
        raise Http404
    usr.premium = True
    usr.save()
    return HttpResponseRedirect('/')

@login_required
def current_auctions_view(request):
    products = Product.objects.filter(user__email=request.user.email)
    context = {'products': products}
    return render(request, 'users/current_auctions.html', context)

@login_required
def won_auctions_view(request):
    products = Product.objects.filter(winner=str(request.user.email), disponible=False)
    context = {'products': products}
    return render(request, 'users/won_auctions.html', context)

@login_required
def lost_auctions_view(request):
    products = Product.objects.filter(user__email=request.user.email)
    products = products.difference(Product.objects.filter(winner=str(request.user.email)))
    context = {'products': products}
    return render(request, 'users/lost_auctions.html', context)

@login_required
def my_auctions_view(request):
    try:
        products = Product.objects.filter(profile=request.user.profile)
    except:
        products = Product.objects.none()
    context = {'products': products}
    return render(request, 'users/my_auctions.html', context)

