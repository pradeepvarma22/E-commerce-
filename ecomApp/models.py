from django.db import models
from accounts.models import Customer
# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_price = models.FloatField()
    product_image = models.ImageField(null=False,blank=True)
    createdon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    
    def __str__(self):
        return "Order id : "+str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    phoneno = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)

    
