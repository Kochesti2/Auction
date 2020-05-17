from django.urls import path, include

from users import views

#app_name = 'usr'
urlpatterns = [
    # path('detail/<int:id>/',views.users_detail_view, name ='detials'),
    path('create/',views.register_page,name = 'create'),
    path('logout/',views.logout_view, name = 'log-out-view'),
    path('', include('django.contrib.auth.urls')),
    # path('profileit/', views.UserCreateProfileView, name="profile"),
]