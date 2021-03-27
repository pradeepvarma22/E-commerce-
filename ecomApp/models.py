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


class Cart(models.Model):
    total = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Cart: " + str(self.id)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True,blank=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(default=1,null=True,blank=True)
    line_total = models.IntegerField(null=True,blank=True,default=0)


    def __str__(self):
        return str(self.id)

