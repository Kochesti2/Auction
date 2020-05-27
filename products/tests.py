from datetime import datetime, timedelta
from django.test import TestCase

# Create your tests here.
from products.models import Product


class AgeMethodTest(TestCase):
    def test_get_product_age_today(self):
        init_date = datetime.date(datetime.now())

        product = Product(name="Test",description="Test_description",price = 300, min_increment=1,profile=None,init_date = init_date )
        self.assertEqual(product.get_product_age(),0,"Should return 0")

    def test_get_product_age_within_week_two_days_ago(self):
        delta = timedelta(days=2)
        days_ago = datetime.now() - delta
        init_date = datetime.date(days_ago)

        product = Product(name="Test",description="Test_description",price = 300, min_increment=1,profile=None,init_date = init_date )
        self.assertEqual(product.get_product_age(),0,"Should return 0")

    def test_get_product_age_within_week_seven_days_ago(self):
        delta = timedelta(days=7)
        days_ago = datetime.now() - delta
        init_date = datetime.date(days_ago)

        product = Product(name="Test",description="Test_description",price = 300, min_increment=1,profile=None,init_date = init_date )
        self.assertEqual(product.get_product_age(),0,"Should return 0")

    def test_get_product_age_within_month_eight_days_ago(self):
        delta = timedelta(days=8)
        days_ago = datetime.now() - delta
        init_date = datetime.date(days_ago)

        product = Product(name="Test",description="Test_description",price = 300, min_increment=1,profile=None,init_date = init_date )
        self.assertEqual(product.get_product_age(),1,"Should return 1")

    def test_get_product_age_within_month_30_days_ago(self):
        delta = timedelta(days=30)
        days_ago = datetime.now() - delta
        init_date = datetime.date(days_ago)

        product = Product(name="Test",description="Test_description",price = 300, min_increment=1,profile=None,init_date = init_date )
        self.assertEqual(product.get_product_age(),1,"Should return 1")

    def test_get_product_age_more_than_30_days_1(self):
        delta = timedelta(days=31)
        days_ago = datetime.now() - delta
        init_date = datetime.date(days_ago)

        product = Product(name="Test",description="Test_description",price = 300, min_increment=1,profile=None,init_date = init_date )
        self.assertEqual(product.get_product_age(),2,"Should return 2")

    def test_get_product_age_more_than_30_days_2(self):
        delta = timedelta(days=100)
        days_ago = datetime.now() - delta
        init_date = datetime.date(days_ago)

        product = Product(name="Test",description="Test_description",price = 300, min_increment=1,profile=None,init_date = init_date )
        self.assertEqual(product.get_product_age(),2,"Should return 2")


    def test_get_product_age_if_init_date_is_future(self):
        init_date = datetime.date(datetime(2100,1,1))

        product = Product(name="Test",description="Test_description",price = 300, min_increment=1,profile=None,init_date = init_date )
        self.assertEqual(product.get_product_age(),-1,"Should return -1")

class TimeLeftMethodTest(TestCase):

    def test_time_left_to_end(self):
        delta = timedelta(days=5)
        days_ago = datetime.now() - delta
        days_after = datetime.now() + delta
        init_date = datetime.date(days_ago)
        end_date = datetime.date(days_after)

        product = Product(name="Test",description="Test_description",price = 300,end_date=end_date, min_increment=1,profile=None,init_date = init_date )
        self.assertGreaterEqual(product.time_left_to_end(),0,"Days left shouldn't be less than 0")

    def test_time_left_to_end_inverted(self):
        delta = timedelta(days=5)
        days_after = datetime.now() - delta
        days_ago = datetime.now() + delta
        init_date = datetime.date(days_ago)
        end_date = datetime.date(days_after)

        product = Product(name="Test",description="Test_description",price = 300,end_date=end_date, min_increment=1,profile=None,init_date = init_date )
        self.assertGreaterEqual(product.time_left_to_end(),0,"Days left shouldn't be less than 0")

