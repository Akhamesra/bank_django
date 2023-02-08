from django.test import TestCase,Client
from django.urls import reverse
from django.http import HttpResponse
from profiles.models import Customer_Data,Account_Data,Transactions
from django.views.generic import CreateView
import json


class TestViews(TestCase):


    def setUp(self):
        self.client=Client()
        self.account_management=reverse('profiles:account_management')
        # self.withdraw = reverse('profile:withdraw')
    
    # def test_project_account_managment_GET(self):
    #     response=self.client.get(self.account_management)
    #     self.assertEquals(response.status_code,200)
    #     # self.assertTemplateUsed(response,'profiles/account_details.html')
    
    # def test_project_withdraw_POST(self):
    #     response=self.client.get(self.withdraw)
    #     self.assertEquals(response.status_code,200)
        # self.assertTemplateUsed(response,'profiles/withdraw.html')