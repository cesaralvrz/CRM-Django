from django.db import models
# Importamos User
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    # OneToOneField = solo un usuario por cliente
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
            ('Indoor', 'Indoor'),
            ('Out door', 'Out door'),
        )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
            ('Pending', 'Pending'),
            ('Out for Delivery', 'Out for Delivery'),
            ('Delivered', 'Delivered'),
        )
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True) 
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    # Para poder visualizar el nombre del pedido
    def __str__(self):
        return self.product.name

