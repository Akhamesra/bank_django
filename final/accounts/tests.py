from django.test import SimpleTestCase
from django.urls import reverse,resolve
from . import views

class TestUrls(SimpleTestCase):

    def test_url_is_resolved_login(self):
        url = reverse('accounts:login')
        self.assertEquals(resolve(url).func,views.login)

    def test_url_is_resolved_register(self):
        url2 = reverse('accounts:register')
        self.assertEquals(resolve(url2).func,views.register)
    
        