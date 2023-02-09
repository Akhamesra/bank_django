from django.test import TestCase,Client
from django.urls import reverse
from profiles.models import Customer_Data,Account_Data
from profiles.views import home,user_details,show_details,deposit,display_menu,get_function_chosen,account_management,get_account_action,withdraw,deposit,stat_gen,get_transaction_action,admin_view,transfer,error
from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse,resolve


class TestUrls(SimpleTestCase):

    def test_url_is_resolved_home(self):
        url = reverse('profiles:home')
        self.assertEquals(resolve(url).func,home)

    def test_url_is_resolved_user_details(self):
        url = reverse('profiles:user_details')
        self.assertEquals(resolve(url).func,user_details)
    
    def test_url_is_resolved_show_details(self):
        url = reverse('profiles:show_details')
        self.assertEquals(resolve(url).func,show_details)
    
    def test_url_is_resolved_deposit(self):
        url = reverse('profiles:deposit')
        self.assertEquals(resolve(url).func,deposit)

    def test_url_is_resolved_account_management(self):
        url = reverse('profiles:account_management')
        self.assertEquals(resolve(url).func,account_management)
    
    def test_url_is_resolved_withdraw(self):
        url = reverse('profiles:withdraw')
        self.assertEquals(resolve(url).func,withdraw)

    def test_url_is_resolved_stat_gen(self):
        url = reverse('profiles:stat_gen')
        self.assertEquals(resolve(url).func,stat_gen)
    def test_url_is_resolved_admin_view(self):
        url = reverse('profiles:admin_view')
        self.assertEquals(resolve(url).func,admin_view)
    def test_url_is_resolved_transfer(self):
        url = reverse('profiles:transfer')
        self.assertEquals(resolve(url).func,transfer)

    def test_url_is_resolved_error(self):
        url = reverse('profiles:error')
        self.assertEquals(resolve(url).func,error)
    
        
class TestViews(TestCase):
    def setUp(self):
        self.client=Client()
        self.account_management=reverse('profiles:account_management')
        self.withdraw = reverse('profiles:withdraw')
    
    def test_project_account_managment_GET(self):
        response=self.client.get(self.account_management)
        self.assertEquals(response.status_code,200)


class TestCustomerModel(TestCase):
    def test_model_str(self):
        name = Customer_Data.objects.create(Name='test1')
        self.assertEqual(str(name),"test1")

class TestAccountModel(TestCase):
    def test_model_str(self):
        user1 = Customer_Data.objects.create(Name='test1')
        accno = Account_Data.objects.create(Accno='567890',Balance='10',Owner=user1)
        self.assertEqual(str(accno),'567890')



