from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from users import views

#app_name = 'usr'
urlpatterns = [
    # path('detail/<int:id>/',views.users_detail_view, name ='detials'),
    path('create/',views.register_page,name = 'create'),
    path('logout/',views.logout_view, name = 'log-out-view'),
    # path('password_reset/',views.password_reset_view, name = 'passwor-reset'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_confirm/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('create_auction/',views.new_auction_page, name = 'create-auction'),
    path('profileit/', views.profile_change, name='profileit'),
    path('get_premium/', views.get_premium, name='get_premium'),
    path('got_premium/', views.get_premium_after, name='got_premium'),
    path('', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)