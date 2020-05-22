from django.contrib.auth import get_user_model, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest, Http404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required


from products.models import Product, ProductImage
from django.contrib.auth.decorators import login_required

# def users_detail_view(request,id):
#    obj = get_object_or_404(User, id =id)
#    context = {
#          'id':obj.id,
#          'name':obj.name,
#          'surname':obj.surname,
#          'mail':obj.email
#    }
#    return render(request, "users/users_home.html", context)
#







# def UserCreateProfileView(request):
#     my_form = UserProfileForm(request.POST)
#     print("request -" , request)
#     # if form.is_valid():
#     #     form.save()
#     #     form = UserProfileForm()
#     # else:
#     #     print("form is not valid")
#
#     context = {
#         'from': my_form
#     }
#     return render(request, "users/user_profile_create.html", context)
#

from users.forms import RegisterForm, new_auction_form, Profile_user_form
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
        return HttpResponseRedirect('/')

    return render(request, "registration/user_create.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def new_auction_page(request):
    print(request.method)
    form = new_auction_form(request.POST or None)
    context = {
        "form": form
    }

    # print("user è ", request.user.first_name)
    # print("profile è ", Profile.objects.get(user=request.user))
    try:
        prof = Profile.objects.get(user=request.user)
    except:
        # return HttpResponseRedirect('/users/profile')
        raise Http404

    NumeroProdottiPerCliente = Product.objects.filter(profile=prof).count()
    print(NumeroProdottiPerCliente)
    if NumeroProdottiPerCliente >= 3 and not request.user.premium:
        return render(request, "users/credit_card.html", {})

    if form.is_valid():
        name  = form.cleaned_data.get("name")
        description = form.cleaned_data.get("description")
        price = form.cleaned_data.get("price")
        min_increment = form.cleaned_data.get("min_increment")
        end_date = form.cleaned_data.get("end_date")
        p = Product(name=name,description= description,price=price,min_increment=min_increment,end_date=end_date,final_price=price,profile = prof)
        p.save()

        for file in request.FILES.getlist('images'):
            instance = ProductImage(
                product=ProductImage.objects.get(request.user.id),
                image=file
            )
            instance.save()
        return HttpResponseRedirect('/')

    return render(request, "users/new_auction.html", context)






@login_required
def profile_change(request):
    print(request.method)

    try:
        usr = request.user
    except:
        # return HttpResponseRedirect('/users/profile')
        raise Http404

    try:
        usr.profile
        form = Profile_user_form(request.POST or None, instance=get_object_or_404(Profile, id=request.user.id))
    except:
        form = Profile_user_form(request.POST or None)

    if form.is_valid():
        country  = form.cleaned_data.get("country")
        city = form.cleaned_data.get("city")
        street = form.cleaned_data.get("street")
        zip_code = form.cleaned_data.get("zip_code")
        image = form.cleaned_data.get("image")
        print("image",image)
        p = Profile.objects.create_update_Profile(usr,country,city,street,zip_code,image)

        return HttpResponseRedirect('/')
    else:
        form = Profile_user_form()

    context = {
        "form": form,
    }

    return render(request, "users/profile_page.html", context)


def get_premium(request):
    return render(request, "users/credit_card.html", {})

def get_premium_after(request):
    try:
        usr = User.objects.get(id=request.user.id)
    except:
        raise Http404


    usr.premium = True
    usr.save()

    return HttpResponseRedirect('/')


