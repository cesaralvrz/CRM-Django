from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm, ProductForm
from .filters import OrderFilter
# Importamos la función del archivo decorators.py
from .decorators import unauthenticated_user


# Agregamos la función de decorators.py
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')

    context = {'form': form }
    return render(request, 'accounts/register.html', context)

# Agregamos la función de decorators.py
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    # Import de logout
    logout(request)
    return redirect('login')

# Es necesario esta en tu cuenta para entrar a esta página
# Sino estas en una cuenta serás enviado a la login page
@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 
    'total_orders': total_orders, 'delivered': delivered, 'pending': pending}

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})  


@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()

    # Asignamos a la variable 'myFilter' la clase que importamos
    # Los datos de 'orders' serán filtrados
    myFilter = OrderFilter(request.GET, queryset=orders)
    # Recreamos la variable 'orders' para los que cumplen los parámetros
    orders = myFilter.qs

    # Agregamos la variable al diccionario
    context = {'customer': customer, "orders": orders, "order_count": order_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def createOrder(request, pk):
    # Creamos el Order Form Set (extra = número de línes más)
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=6)
    customer = Customer.objects.get(id=pk)
    # Asignamos a la variable formset el valor de OrderFormSet y que este indicado el customer
    # El Query set es para que no se incluyan los pedidos que ya existen
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset .save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # Para no crear un nuevo y que se cambie el selccionado, usamos instance
        form = OrderForm(request.POST, instance=order)
        # Si nuestro formulario es válida
        if form.is_valid():
            form.save()
            # Nos devuelve al dashboard
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/update.html', context)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'order': order} 
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
def createCustomer(request):
    # Creamos la variable form y le asignamos la 'OrderForm()'
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        # Si nuestro formulario es válida
        if form.is_valid():
            form.save()
            # Nos devuelve al dashboard
            return redirect('/')

    # Agregamos la variable a nuestro diccionario
    context = {'form': form}
    return render(request, 'accounts/update.html', context)


@login_required(login_url='login')
def updateCustomer(request, pk):
    order = Customer.objects.get(id=pk)
    form = CustomerForm(instance=order)

    if request.method == 'POST':
        # Para no crear un nuevo y que se cambie el selccionado, usamos instance
        form = CustomerForm(request.POST, instance=order)
        # Si nuestro formulario es válida
        if form.is_valid():
            form.save()
            # Nos devuelve al dashboard
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/update.html', context)


@login_required(login_url='login')
def createProduct(request):
    # Creamos la variable form y le asignamos la 'OrderForm()'
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        # Si nuestro formulario es válida
        if form.is_valid():
            form.save()
            # Nos devuelve al dashboard
            return redirect('/')

    # Agregamos la variable a nuestro diccionario
    context = {'form': form}
    return render(request, 'accounts/update.html', context)
