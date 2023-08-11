from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.client_home, name="client-home"),
    path("supplier/", views.supplier_home, name="supplier-home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/client/", views.ClientSignUpView.as_view(), name="client-signup"),
    path("signup/supplier/", views.SupplierSignUpView.as_view(), name="supplier-signup"),
    path('logout/', views.LogoutView.as_view(template_name="pedidos/logout.html"), name="logout"),
    path("supplier/item/create/", views.create_item, name="create-item"),
    path("item/<int:item_id>/order/", views.create_order, name="create-order"),
    path("item/<int:item_id>/order/edit/<int:order_id>/", views.edit_order, name="edit-order"),
    path("item/<int:item_id>/order/edit/<int:order_id>/delete/", views.delete_order, name="delete-order"),
    path("item/<int:item_id>/", views.client_order_detail, name="client-order-detail"),
    path("supplier/item/<int:item_id>/", views.supplier_item_detail, name="supplier-item-detail"),
    path("supplier/item/<int:item_id>/edit/", views.edit_item, name="edit-item"),
    path("supplier/item/<int:item_id>/delete/", views.delete_item, name="delete-item"),
    path("supplier/item/<int:item_id>/order/edit/<int:order_id>/", views.manage_order_create, name="manage-order"),
]