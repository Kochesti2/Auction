from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from products import views

urlpatterns = [
    path('<int:id>/',views.product_detail_view, name ='product-detials'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

