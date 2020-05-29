from django.contrib import admin
from django.contrib import admin
from .models import Comment
# Register your models here.
from products.models import Product, ProductImage

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Comment)
