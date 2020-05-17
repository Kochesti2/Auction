from django.contrib.auth import get_user_model, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
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

from users.forms import RegisterForm

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
