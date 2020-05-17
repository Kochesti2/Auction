from django.urls import path, include

from products import views

urlpatterns = [
    path('<int:id>/',views.product_detail_view, name ='product-detials')
]