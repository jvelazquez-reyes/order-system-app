from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Define user roles (client, supplier) inheriting from the generic Django User model
class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)

class Client(models.Model):
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
    # user field defined as a primary key of Client model as an extension of the generic User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='client')
    code = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True)
    address = models.CharField(max_length=100)
    client_type = models.CharField(
        max_length=1,
        choices=CLIENT_CHOICES,
        default=NORMAL,
    )

class Supplier(models.Model):
    # user field defined as a primary key of Supplier model as an extension of the generic User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='supplier')
    address = models.CharField(max_length=100)
    items_supplied = models.CharField(max_length=100)


# Model for items
class Item(models.Model):
    # code field is the primary key
    code = models.IntegerField(primary_key=True)
    description = models.TextField()
    price = models.FloatField()
    # supplier field define a many-to-one relationship
    # This means that a supplier can be associated with many Item objects
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='items')

# Model for orders
class Order(models.Model):
    # orderNo field is the primary key
    orderNo = models.IntegerField(primary_key=True)
    # client field define a many-to-one relationship
    # This means that a client can be associated with many Order objects
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(default=timezone.now)
    is_urgent = models.BooleanField(default=False)
    distribution_center = models.BooleanField(default=False)
    branch = models.BooleanField(default=False)
    associated_company = models.BooleanField(default=False)
    # item field define a many-to-one relationship
    # This means that an item can be associated with many Order objects
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField()

# Managing order by supplier
class ManageOrder(models.Model):
    # user field defined as a primary key of ManageOrder model as an extension of Order model
    # one-to-one relationship
    orderNo = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True, related_name='orders')
    dispatched_at = models.DateTimeField(default=timezone.now)
    warehouse = models.CharField(max_length=50)
    reference = models.CharField(max_length=50)
    branch_code = models.IntegerField(null=True)
    details = models.CharField(max_length=200)
    



