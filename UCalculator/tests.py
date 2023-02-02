from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, calculator


# Create your tests here.
class HomeTests(TestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
      
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

class CalculatorTests(TestCase):
    def test_calculator_view_status_code(self):
        url = reverse('calculator')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
      
    def test_calculator_url_resolves_calculator_view(self):
        view = resolve('/calculator')
        self.assertEquals(view.func, calculator)