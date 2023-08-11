from django.contrib import admin
from .models import User, Item, Order, Client, Supplier, ManageOrder

# Register your models here.
admin.site.register(User)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Client)
admin.site.register(Supplier)
admin.site.register(ManageOrder)