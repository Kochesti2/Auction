from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from users import views


urlpatterns = [
    # path('detail/<int:id>/',views.users_detail_view, name ='detials'),
    path('create/',views.register_page,name = 'create'),
    path('logout/',views.logout_view, name = 'log-out-view'),
    path('create_auction/',views.new_auction_page, name = 'create-auction'),
    path('profileit/', views.profile_change, name='profileit'),
    path('get_premium/', views.get_premium, name='get_premium'),
    path('got_premium/', views.get_premium_after, name='got_premium'),
    path('current_auctions/', views.current_auctions_view, name='current-auctions'),
    path('won_auctions/', views.won_auctions_view, name='won-auctions'),
    path('lost_auctions/', views.lost_auctions_view, name='lost-auctions'),
    path('my_auctions/', views.my_auctions_view, name='my-auctions'),
    path('', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)