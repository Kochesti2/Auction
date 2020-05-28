from datetime import datetime
from django.test import TestCase, Client

# Create your tests here.
# use : python manage.py test users
from django.urls import reverse

from products.models import Product
from users.admin import User
from django.contrib.auth import get_user_model

from users.models import Profile

User = get_user_model()
class TestCurrentAuctionsView(TestCase):
    def setUp(self):
        #buyer
        email = "prova@prova.com"
        first_name = "testname"
        last_name = "testlastname"
        password = "unimore"
        tel = 3556958
        self.u = User.objects.create_user( email, first_name, last_name, password, tel)

        #seller
        email = "prova1@prova1.com"
        first_name = "testname1"
        last_name = "testlastname1"
        password = "unimore"
        tel = 3556959
        self.v = User.objects.create_user( email, first_name, last_name, password, tel)

        # other buyer
        email = "buyer2@buyer2.com"
        first_name = "testname3"
        last_name = "testlastname3"
        password = "unimore"
        tel = 3556958
        self.t = User.objects.create_user(email, first_name, last_name, password, tel)

    def myLoginBuyer(self):
        self.client.login(username='prova@prova.com', password='unimore')

    def myLoginSeller(self):
        self.client.login(username='prova1@prova1.com', password='unimore')

    def myLoginOtherBuyer(self):
        self.client.login(username='buyer2@buyer2.com', password='unimore')

    def createproduct(self,who):
        p =  Product.objects.create(name="Test", description="Test_description",  price = 300, min_increment=1, end_date = datetime.date(datetime(2100,1,1)),  final_price=300, profile=who)
        return p

    def test_link_with_no_user(self):
        response = self.client.get(reverse('current-auctions'))
        self.assertEqual(response.status_code, 302, "Needs to be redirected")

    def test_link_with_user(self):
        '''test if links doen't redirect me when i am authenticated'''
        self.myLoginBuyer()
        response = self.client.get(reverse('current-auctions'))
        self.assertEqual(response.status_code, 200, "Authenticated user should return 200")

    def test_when_there_are_no_my_current_auctions(self):
        self.myLoginBuyer()
        response = self.client.get(reverse('current-auctions'))
        self.assertQuerysetEqual(response.context['products'], [], "Should return empty query")

    def test_when_there_is_one_product_and_bidded(self):
        country  = "Italy"
        city = "Rome"
        street = "Curie 39"
        zip_code = "42536"
        photo = None
        self.uprofile = Profile.objects.create(user=self.u,country=country,city=city,street=street,zip_code=zip_code,photo=photo)

        country  = "Italy1"
        city = "Rome1"
        street = "Curie 391"
        zip_code = "425361"
        photo = None
        self.vprofile = Profile.objects.create(user=self.v,country=country,city=city,street=street,zip_code=zip_code,photo=photo)

        self.myLoginSeller()
        who = self.vprofile
        product = self.createproduct(who)
        self.client.logout()
        self.myLoginBuyer()
        product.user.add(self.u)
        response = self.client.get(reverse('current-auctions'))
        self.assertEqual(list(response.context['products']), list(Product.objects.all()), "Should return one queryset")

    def test_when_there_is_one_product_but_not_bidded(self):
        country = "Italy"
        city = "Rome"
        street = "Curie 39"
        zip_code = "42536"
        photo = None
        self.uprofile = Profile.objects.create(user=self.u, country=country, city=city, street=street,
                                               zip_code=zip_code, photo=photo)

        country = "Italy1"
        city = "Rome1"
        street = "Curie 391"
        zip_code = "425361"
        photo = None
        self.vprofile = Profile.objects.create(user=self.v, country=country, city=city, street=street,
                                               zip_code=zip_code, photo=photo)

        self.myLoginSeller()
        self.client.logout()
        self.myLoginBuyer()

        response = self.client.get(reverse('current-auctions'))
        self.assertEqual(list(response.context['products']), [], "Should return empty queeyset")

    def test_when_there_is_one_product_bidded_but_by_other_user(self):
        country = "Italy"
        city = "Rome"
        street = "Curie 39"
        zip_code = "42536"
        photo = None
        self.uprofile = Profile.objects.create(user=self.u, country=country, city=city, street=street,
                                               zip_code=zip_code, photo=photo)

        country = "Italy1"
        city = "Rome1"
        street = "Curie 391"
        zip_code = "425361"
        photo = None
        self.vprofile = Profile.objects.create(user=self.t, country=country, city=city, street=street,
                                               zip_code=zip_code, photo=photo)

        country = "Italy2"
        city = "Rome2"
        street = "Curie 392"
        zip_code = "425362"
        photo = None
        self.tprofile = Profile.objects.create(user=self.v, country=country, city=city, street=street,
                                               zip_code=zip_code, photo=photo)

        self.myLoginSeller()
        who = self.vprofile
        product = self.createproduct(who)
        self.client.logout()
        self.myLoginBuyer()
        product.user.add(self.u)
        self.client.logout()
        self.myLoginOtherBuyer()
        response = self.client.get(reverse('current-auctions'))
        self.assertEqual(list(response.context['products']), list([]), "Should return empty queryset")

    def test_user_is_authenticated_and_doent_have_profile(self):
        country = "Italy1"
        city = "Rome1"
        street = "Curie 391"
        zip_code = "425361"
        photo = None
        self.vprofile = Profile.objects.create(user=self.t, country=country, city=city, street=street,
                                               zip_code=zip_code, photo=photo)

        self.myLoginSeller()
        who = self.vprofile
        self.createproduct(who)
        self.client.logout()
        self.myLoginBuyer()
        response = self.client.get(reverse('current-auctions'))
        self.assertEqual(list(response.context['products']), list([]), "Should return empty queryset")