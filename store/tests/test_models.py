from unicodedata import category
from django.test import TestCase
from store.models import Category, Product
from django.contrib.auth.models import User

class TestCategoriesModel(TestCase):
    
    def setUp(self):
        self.data1 = Category.objects.create(name='toys', slug='toys')

    def test_category_model_entry(self):
        """Test category model data insertion/types/field attributes"""
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_entry(self):
        """Test category model default name"""
        data = self.data1
        self.assertEqual(str(data), 'toys')

class TestProductsModel(TestCase):
    def setUp(self):
        Category.objects.create(name='toys', slug='toys')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id = 1, title='ball', created_by_id=1, slug='ball', price='9.99', image='ball')

    def test_product_model_entry(self):
        """Test category model data insertion/types/field attributes"""
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'ball')