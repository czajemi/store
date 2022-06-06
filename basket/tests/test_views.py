from account.models import UserBase
from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product

class TestBasketView(TestCase):
    def setUp(self):
        Category.objects.create(name='toys', slug='toys')
        UserBase.objects.create(email='admin@emilka.com')
        Product.objects.create(category_id = 1, title='ball', created_by_id=1, slug='ball', price='9.99', image='ball_AWCNJFN')
        Product.objects.create(category_id = 1, title='bone', created_by_id=1, slug='bone', price='10.01', image='bone')
        self.client.post(reverse('basket:basket_add'), {"productid": 1, "productqty": 1, "action": "post"}, xhr=True)
        self.client.post(reverse('basket:basket_add'), {"productid": 2, "productqty": 2, "action": "post"}, xhr=True)

    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding items to the basket
        """
        response = self.client.post(reverse('basket:basket_add'), {"productid": 1, "productqty": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(reverse('basket:basket_add'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 3})

    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(reverse('basket:basket_delete'), {"productid": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '9.99'})

    def test_basket_update(self):
        """
        Test updating items from the basket
        """
        response = self.client.post(reverse('basket:basket_update'), {"productid": 2, "productqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '20.00'})