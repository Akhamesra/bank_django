from django.test import SimpleTestCase
from django.urls import reverse,resolve
from .. import views

class TestUrls(SimpleTestCase):

    def test_url_is_resolved_login(self):
        url = reverse('accounts:signin')
        self.assertEquals(resolve(url).func,views.sign_in)

    def test_url_is_resolved_register(self):
        url2 = reverse('accounts:signup')
        self.assertEquals(resolve(url2).func,views.register)

    def test_url_is_resolved_logout(self):
        url3 = reverse('accounts:logout')
        self.assertEquals(resolve(url3).func,views.logout_view)
    

    
    
        