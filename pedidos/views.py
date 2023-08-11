from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView
from .models import User, Item, Order
from .forms import ClientSignUpForm, SupplierSignUpForm, LoginForm, ItemForm, OrderForm, ManageOrderOneForm, ManageOrderTwoForm, ManageOrderThreeForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import client_required, supplier_required

# Views for different user roles
class ClientSignUpView(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = 'pedidos/client_signup.html'

    # Merge context data of parent Class and current Class to pass it to the template
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('client-home')
    
class SupplierSignUpView(CreateView):
    model = User
    form_class = SupplierSignUpForm
    template_name = 'pedidos/supplier_signup.html'

    # Merge context data of parent Class and current Class to pass it to the template
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'supplier'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('supplier-home')
    
# Login view
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'pedidos/login.html'

    # Merge context data of parent Class and current Class to pass it to the template
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    # Redirecting after successfull login
    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_client:
                return reverse('client-home')
            elif user.is_supplier:
                return reverse('supplier-home')
        else:
            return reverse('login')
        
# Logout view
class LogoutView(TemplateView):
    template_name = 'pedidos/logout.html'
        
@login_required
@client_required
def client_home(request):
    # Retrieve items published by Supplier and list them in the Client dashboard
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'pedidos/client_home.html', context)

@login_required
@supplier_required
def supplier_home(request):
    # Retrieve items published and list them in the Supplier dashboard
    items = Item.objects.filter(supplier=request.user.supplier)
    context = {
        'items': items,
    }
    return render(request, 'pedidos/supplier_home.html', context)

@login_required
@supplier_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        # Validate the form before commiting database operations
        if form.is_valid():
            item = form.save(commit=False)
            item.supplier = request.user.supplier
            item.save()
            return redirect('supplier-home')
    else:
        form = ItemForm()
    return render(request, 'pedidos/create_item.html', {'form': form})

@login_required
@supplier_required
def delete_item(request, item_id):
    item = Item.objects.get(code=item_id)
    item.delete()

    return redirect('supplier-home')


@login_required
@client_required
def create_order(request, item_id):
    item = Item.objects.get(code=item_id)
    if Order.objects.filter(item=item, client=request.user.client).exists():
        return redirect('client-home')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        # Validate the form before commiting database operations
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user.client
            order.item = item
            order.save()
            return redirect('client-home')
    else:
        form = OrderForm()
    return render(request, 'pedidos/create_order.html', {'form': form, 'item': item})

@login_required
@client_required
def edit_order(request, item_id, order_id):
    # Getting item and order by their id
    item = Item.objects.get(code=item_id)
    order = Order.objects.get(orderNo=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('client-home')
    else:
        # Fill in the form with existing order
        form = OrderForm(instance=order)
    return render(request, 'pedidos/create_order.html', {'form': form, 'item': item, 'order': order})

@login_required
@client_required
def delete_order(request, item_id, order_id):
    order = Order.objects.get(orderNo=order_id)
    order.delete()

    return redirect('client-home')

@login_required
@client_required
def client_order_detail(request, item_id):
    # Getting item by id to show its details
    item = Item.objects.get(code=item_id)
    # Define variable ordered to determine if the item has been ordered
    # This variable is passed to templated through context data
    # If ordered == True the html template will render the option to edit the order
    # If ordered == False the html template will render the option to place an order 
    if Order.objects.filter(item=item, client=request.user.client).exists():
        order = Order.objects.get(item=item, client=request.user.client)
        ordered = True
    else:
        order = None
        ordered = False
    # All data passed to template through context data
    context = {
        'item': item,
        'order': order,
        'ordered': ordered
    }
    return render(request, 'pedidos/client_order_detail.html', context)

@login_required 
@supplier_required
def supplier_item_detail(request, item_id):
    # Getting item by id to show its details
    item = Item.objects.get(code=item_id)
    if item.supplier != request.user.supplier:
        return redirect('supplier-home')
    orders = Order.objects.filter(item=item)
    # All data passed to template through context data
    context = {
        'item': item,
        'orders': orders
    }
    return render(request, 'pedidos/supplier_item_detail.html', context)

@login_required
@supplier_required
def edit_item(request, item_id):
    # Getting item by its id
    item = Item.objects.get(code=item_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('supplier-home')
    else:
        # Fill in the form with existing item data
        form = ItemForm(instance=item)
    return render(request, 'pedidos/create_item.html', {'form': form, 'item': item})

# When Client place an order, the supplier will have the option to manage this order
@login_required
@supplier_required
def manage_order_create(request, item_id, order_id):
    # Getting item and order by their id
    item = Item.objects.get(code=item_id)
    order = Order.objects.get(orderNo=order_id)

    if request.method == 'POST':        
        # Form order to center of distribution
        form_one = ManageOrderOneForm(request.POST)
        if form_one.is_valid():
            manage_order_one = form_one.save(commit=False)
            manage_order_one.save()
            return redirect('supplier-home')
        
        # Form order to branch
        form_two = ManageOrderTwoForm(request.POST)
        if form_two.is_valid():
            manage_order_two = form_two.save(commit=False)
            manage_order_two.save()
            return redirect('supplier-home')
        
        # Form order to associated company
        form_three = ManageOrderThreeForm(request.POST)
        if form_two.is_valid():
            manage_order_three = form_three.save(commit=False)
            manage_order_three.save()
            return redirect('supplier-home')
    else:
        form_one = ManageOrderOneForm()
        form_two = ManageOrderTwoForm()
        form_three = ManageOrderThreeForm()
    return render(request, 'pedidos/manage_order.html', {'form_one': form_one,
                                                         'form_two': form_two,
                                                         'form_three': form_three,
                                                         'item': item,
                                                         'order': order})