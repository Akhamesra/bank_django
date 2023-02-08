from django.test import TestCase
from profiles.models import Customer_Data,Account_Data,Transactions

class TestAppModel(TestCase):
    def test_model_str(self):
        name = Customer_Data.objects.create(name='test1')
        self.assertEqual(str(name),"user1")