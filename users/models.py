import os
from django.db import models
from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager )

class UserManager(BaseUserManager):
    def create_user(self, email, first_name , last_name, password=None, tel="", is_premium = False,  is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password) # change user password
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.tel = tel
        user_obj.premium = is_premium
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email,first_name, last_name, password=None):
        user = self.create_user(
                email,
                first_name,
                last_name,
                password=password,
                is_staff=True,
                 is_premium=True
        )
        return user

    def create_premiumuser(self, email,first_name, last_name, password=None):
        user = self.create_user(
                email,
                first_name,
                last_name,
                password=password,
                is_premium=True
        )
        return user

    def create_superuser(self, email, first_name, last_name, password=None, tel=""):
        user = self.create_user(
                email,
                first_name,
                last_name,
                password=password,
                tel = tel,
                is_staff=True,
                is_admin=True,
                is_premium=True
        )
        return user


class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    tel = models.CharField(max_length=50, blank = True , null= True)
    premium     = models.BooleanField(default=False)
    is_active      = models.BooleanField(default=True) # can login
    staff       = models.BooleanField(default=False) # staff user non superuser
    admin       = models.BooleanField(default=False) # superuser


    USERNAME_FIELD = 'email' #username
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = UserManager()



    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_premium(self):
        return self.premium



def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class ProfileManager(BaseUserManager):
    def create_update_Profile(self,user,country,city,address,zip_code, photo):
        try:
            p = user.profile
            crt = False
        except Profile.DoesNotExist:
            print("profile doen't exist")
            crt = True

        if crt:
            if photo == None:
                profile = self.create(user=user, country=country, city=city, address=address, zip_code=zip_code,
                                  rating=0)
            else:
                profile = self.create(user=user, country=country, city=city, address=address, zip_code=zip_code,
                                  rating=0,photo=photo)
        else:
            p.country = country
            p.city = city
            p.address = address
            p.zip_code = zip_code
            if photo != None:
                p.photo=photo
            p.save()
            return p
        return profile

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    country = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    address = models.CharField(max_length=254)
    zip_code = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='photos/', blank=True, default='default-profile.jpg')

    objects = ProfileManager()


