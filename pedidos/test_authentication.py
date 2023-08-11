from django.test import TestCase
from django.urls import reverse
from .models import Supplier


class BaseTest(TestCase):
    def setUp(self):
        # Client signup url
        self.client_register_url = reverse('client-signup')
        # Supplier signup url
        self.supplier_register_url = reverse('supplier-signup')

        # Login url
        self.login_url = reverse('login')

        # Logout uel
        self.logout_url = reverse('logout')

        # Create supplier user
        self.supplier_user = {
            'username': 'username',
            'password1': 'micontrasenasecreta', 
            'password2': 'micontrasenasecreta',
            'address': 'calle2',
            'items_supplied': 'items_x',
        }

        # Attempt creating supplier user (missing field)
        self.supplier_user_missing_field = {
            'username': '',
            'password1': 'micontrasenasecreta', 
            'password2': 'micontrasenasecreta',
            'address': 'calle2',
            'items_supplied': 'items_x',
        }

        # Create user - unmatching passwords
        self.supplier_user_wrong_passwords = {
            'username': 'username',
            'password1': 'micontrasenasecreta65', 
            'password2': 'micontrasenasecreta',
            'address': 'calle2',
            'items_supplied': 'items_x',
        }

        return super().setUp()
    
class RegisterTest(BaseTest):
    # User type Client GET request and proper render template 
    def test_client_can_view_signup_page_correct(self):
        response = self.client.get(self.client_register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'pedidos/client_signup.html')

    # User type Supplier GET request and proper render template 
    def test_supplier_can_view_signup_page_correct(self):
        response = self.client.get(self.supplier_register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'pedidos/supplier_signup.html')


    # Create supplier user (expecting "return redirect('supplier-home') status_code = 302")
    def test_can_register_supplier_user(self):
        response = self.client.post(self.supplier_register_url, self.supplier_user, format='text/html')
        self.assertEqual(response.status_code, 302)

    # Create supplier user (expecting "return redirect('supplier-home') status_code = 302")
    def test_cannot_register_supplier_user(self):
        response = self.client.post(self.supplier_register_url, self.supplier_user_missing_field, format='text/html')
        self.assertNotEqual(response.status_code, 302)

    # Create supplier user (expecting "return redirect('supplier-home') status_code = 302")
    def test_cannot_register_supplier_user_wrong_password(self):
        response = self.client.post(self.supplier_register_url, self.supplier_user_wrong_passwords, format='text/html')
        self.assertNotEqual(response.status_code, 302)

class LoginTest(BaseTest):
    # Test GET request and proper login rendering page
    def test_can_access_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pedidos/login.html')

    # Test login success
    def test_login_success(self):
        self.client.post(self.supplier_register_url, self.supplier_user, format='text/html')
        supplier_user = Supplier.objects.filter(address=self.supplier_user['address']).first()
        supplier_user.is_active = True
        supplier_user.save()
        response = self.client.post(self.login_url, self.supplier_user, format='text/html')
        self.assertEqual(response.status_code, 200)

class LogoutTest(BaseTest):
    # Logout GET request and proper render template 
    def test_logout_page_correct(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'pedidos/logout.html')