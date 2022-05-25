from django.conf import settings
from django.http import HttpRequest
from importlib import import_module
from django.contrib.auth.models import User
from store.models import Category, Product
from django.test import Client, TestCase
from django.urls import reverse
from store.views import product_all

class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        Category.objects.create(name='toys', slug='toys')
        User.objects.create(username='admin')
        Product.objects.create(category_id = 1, title='ball', created_by_id=1, slug='ball', price='9.99', image='ball')

    def test_url_allowed_hosts(self):
        """Test allowed hosts"""
        response = self.c.get('/', HTTP_HOST='nothing.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='doggystore.com')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """Test Product response status"""
        response = self.c.get(reverse('store:product_detail', args=['ball']))
        self.assertEqual(response.status_code, 200)

    def test_product_list_url(self):
        """
        Test category response status
        """
        response = self.c.get(
            reverse('store:category_list', args=['toys']))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """Test Category response status"""
        response = self.c.get(reverse('store:category_list', args=['toys']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """Code validation, search HTML for text"""
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>DoggyStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

