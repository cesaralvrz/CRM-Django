from django.forms import ModelForm
# Importamos la creación de usuario de Django
from django.contrib.auth.forms import UserCreationForm 
# Importamos el User Model (Que vemos en el admin panel)
from django.contrib.auth.models import User
# Importamos los formularios de Django
from django import forms

from .models import *

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'  

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone'] 

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price'] 

# Creamos la clase
class CreateUserForm(UserCreationForm):
    class Meta:
        # Asignamos a la variable model el import que hicimos anteriormente
        model = User
        # Vamos a asignar los campos que desiamos del model en una lista
        fields = ['username', 'email', 'password1', 'password2']
