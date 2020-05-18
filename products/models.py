from datetime import datetime

from django.db import models
from django.template.defaultfilters import slugify

from users.models import User
from users.models import Profile

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=500)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    min_increment = models.DecimalField(decimal_places=2, max_digits=10,default=0.5)
    init_date = models.DateField(default=datetime.now, blank=True)
    end_date = models.DateField()
    winner = models.CharField(max_length=254, blank = True,null=True)
    final_price = models.DecimalField(decimal_places=2, max_digits=10, blank = True,null=True)
    images = models.ImageField(default='default.png',blank=True)
    rating = models.FloatField(default = 0,blank = True,null=True)

    user = models.ManyToManyField(User,blank = True)#interested
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


# def get_image_filename(instance, filename):
#     name = instance.product.name
#     slug = slugify(name)
#     return "product_images/%s-%s" % (slug, filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product.name