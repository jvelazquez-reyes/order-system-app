from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import User, Client, Supplier, Item, Order, ManageOrder
from django import forms
from django.contrib.auth import get_user_model

# To get the current active User model. In this app, our custom User model
User = get_user_model()

# Client signup form
class ClientSignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    code = forms.CharField(widget=forms.TextInput())
    photo = forms.ImageField(widget=forms.FileInput())
    address = forms.CharField(widget=forms.TextInput())
    # Client type choices
    NORMAL = '1'
    PLATA = '2'
    ORO = '3'
    PLATINO = '4'
    CLIENT_CHOICES = [
        (NORMAL, "Normal"),
        (PLATA, "Plata"),
        (ORO, "Oro"),
        (PLATINO, "Platino"),
    ]
    client_type = forms.CharField(widget=forms.Select(choices=CLIENT_CHOICES))

    # Provide the metadata of the generic User model to the ClientSignupForm
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
    
    # Ensure that all operations (custom Client model that inherits the generic User) are performed
    # in a single database transaction to avoid inconsistencies
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = True
        if commit:
            user.save()
        client = Client.objects.create(user=user, code=self.cleaned_data.get('code'), photo=self.cleaned_data.get('photo'), address=self.cleaned_data.get('address'), client_type=self.cleaned_data.get('client_type'))
        return user

# Supplier form
class SupplierSignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    address = forms.CharField(widget=forms.TextInput())
    items_supplied = forms.CharField(widget=forms.TextInput())

    # Provide the metadata of the generic User model to the SupplierSignupForm
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
    
    # Ensure that all operations (custom Supplier model that inherits the generic User) are performed
    # in a single database transaction to avoid inconsistencies
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_supplier = True
        if commit:
            user.save()
        supplier = Supplier.objects.create(user=user, address=self.cleaned_data.get('address'), items_supplied=self.cleaned_data.get('items_supplied'))
        return user
    
# Login form (same for all user types)
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

# Item form
class ItemForm(forms.ModelForm):
    # Metadata from Item model
    class Meta:
        model = Item
        fields = ('code', 'description', 'price',)
        widgets = {
            'code': forms.NumberInput(),
            'description': forms.Textarea(),
            'price': forms.NumberInput(attrs={'step': 0.01, 'max': 1000000000.0, 'min': 0.0})       
        }

# Create order form
class OrderForm(forms.ModelForm):
    # Metadata from Order model
    class Meta:
        model = Order
        fields = ('is_urgent', 'distribution_center', 'branch', 'associated_company', 'quantity',)
        widgets = {
            'is_urgent': forms.CheckboxInput(),
            'distribution_center': forms.CheckboxInput(),
            'branch': forms.CheckboxInput(),
            'associated_company': forms.CheckboxInput(),
            'quantity': forms.TextInput()        
        }

# Manage order one (order to distribution center) form by supplier
class ManageOrderOneForm(forms.ModelForm):
    # Metadata from ManagerOrder model
    class Meta:
        model = ManageOrder
        fields = ('warehouse',)
        widgets = {
            'warehouse': forms.TextInput()        
        }

# Manage order two (order to branch) form by supplier
class ManageOrderTwoForm(forms.ModelForm):
    # Metadata from ManagerOrder model
    class Meta:
        model = ManageOrder
        fields = ('reference', 'branch_code',)
        widgets = {
            'reference': forms.TextInput(),
            'branch_code': forms.NumberInput()     
        }

# Manage order three (order to associated company) form by supplier
class ManageOrderThreeForm(forms.ModelForm):
    # Metadata from ManagerOrder model
    class Meta:
        model = ManageOrder
        fields = ('reference', 'branch_code', 'details')
        widgets = {
            'reference': forms.TextInput(),
            'branch_code': forms.NumberInput(),
            'details': forms.Textarea() 
        }