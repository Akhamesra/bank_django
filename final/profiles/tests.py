from django.test import SimpleTestCase
from django.urls import reverse,resolve
# Create your tests here.

class TestUrls(SimpleTestCase):
    def test_url_is_resolved(self):
        url = reverse("user_details")
        x=resolve(url)
        print(resolve(url))
        self.assertEquals(x.func,views.user_details)