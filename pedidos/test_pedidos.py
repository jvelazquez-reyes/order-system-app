from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class BaseTest(TestCase):
      def setUp(self):
        # Client - home url (list all posted items)
        self.client_items_url = reverse('client-home')
        # Supplier - home url (list all posted items)
        self.supplier_items_url = reverse('supplier-home')
        # Supplier - create item url
        self.supplier_create_item = reverse('create-item')

class SupplierTest(BaseTest):
    # An user that is not autenticated will be redirected when attempting to GET protected routes
    def test_client_cannot_list_items(self):
        response = self.client.get(self.client_items_url)
        self.assertEqual(response.status_code, 302)

    def test_supplier_cannot_list_items(self):
        response = self.client.get(self.supplier_items_url)
        self.assertEqual(response.status_code, 302)

    def test_supplier_cannot_create_item(self):
        response = self.client.get(self.supplier_create_item)
        self.assertEqual(response.status_code, 302)
