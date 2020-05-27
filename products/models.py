from datetime import datetime
from django.db import models
from django.utils import timezone
from users.models import User
from users.models import Profile

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    min_increment = models.DecimalField(decimal_places=2, max_digits=10)
    end_date = models.DateField(verbose_name="Auction end date")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    init_date = models.DateField(default=datetime.now, blank=True)
    winner = models.CharField(max_length=254, blank = True,null=True)
    final_price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=" ", blank = True,null=True)
    rating = models.FloatField(default = 0,blank = True,null=True)
    user = models.ManyToManyField(User,blank = True)#interested
    disponible = models.BooleanField(default=True) #sold or not



    #returns 0 if the auction was posted in last 7 days
    #returns 1 for one month (30 days)
    #returns 2 for older posts
    #return -1 in every other cases
    def get_product_age(self):
        days = int((datetime.date(timezone.localtime(timezone.now())) - self.init_date).days)
        if 0 <= days <= 7:
            return 0
        elif 7 < days <=30:
            return 1
        elif days > 30:
            return 2
        else:
            return -1

    def time_left_to_end(self):
        time = int((self.end_date - datetime.date(timezone.localtime(timezone.now()))).days)
        if time >= 0:
            return time
        else:
            return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', verbose_name='ProductImage', blank=True)

    def __str__(self):
        return self.product.name