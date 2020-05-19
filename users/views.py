from django.contrib.auth import get_user_model, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
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

    try:
        prof = Profile.objects.get(id=request.user.id)
    except:
        # return HttpResponseRedirect('/users/profile')
        raise Http404

    if form.is_valid():
        name  = form.cleaned_data.get("name")
        description = form.cleaned_data.get("description")
        price = form.cleaned_data.get("price")
        min_increment = form.cleaned_data.get("min_increment")
        end_date = form.cleaned_data.get("end_date")
        p = Product(name=name,description= description,price=price,min_increment=min_increment,end_date=end_date,profile = prof)
        p.save()

        for file in request.FILES.getlist('images'):
            instance = ProductImage(
                product=ProductImage.objects.get(request.user.id),
                image=file
            )
            instance.save()
        return HttpResponseRedirect('/')

    return render(request, "users/new_auction.html", context)






# @login_required
# def PersonChange(request):
#     form = Profile_user_form(request.POST)
#
#
#     try:
#         usr = request.user
#     except:
#         # return HttpResponseRedirect('/users/profile')
#         raise Http404
#
#     if form.is_valid():
#         country  = form.cleaned_data.get("country")
#         city = form.cleaned_data.get("city")
#         street = form.cleaned_data.get("street")
#         zip_code = form.cleaned_data.get("zip_code")
#         # image = form.cleaned_data.get("image")
#         p = Profile(user=usr,country=country,city= city,street=street,zip_code=zip_code)
#         try:
#             p.save()
#         except:
#             print("can't save")
#
#         return HttpResponseRedirect('/')
#     else:
#         form = Profile_user_form()
#
#     context = {
#         "form": form
#     }
#
#     return render(request, "users/profile_page.html", context)




class PersonChange(UpdateView,LoginRequiredMixin):
    model = Profile
    template_name = 'users/profile_page.html'
    form_class = Profile_user_form
    # fields = ('first_name', 'middle_name', 'last_name')
    success_url = reverse_lazy('profileit')