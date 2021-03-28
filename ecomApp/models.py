from django.db import models
from accounts.models import Seller,Customer




class Product(models.Model):
    user = models.ForeignKey(Seller,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name



class Checkout(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField()
    NameOnCard = models.CharField(max_length=200,null=True,blank=True)
    Address =models.CharField(max_length=500,null=True,blank=True)
    creditcardnumber = models.CharField(max_length=500,null=True,blank=True)
    city = models.CharField(max_length=300,null=True,blank=True)
    cardExpdate = models.CharField(max_length=300,null=True,blank=True)
    state = models.CharField(max_length=300,null=True,blank=True)
    zip = models.CharField(max_length=300,null=True,blank=True)
    cvv = models.CharField(max_length=300,null=True,blank=True)
    created_at  =  models.DateTimeField ( auto_now_add = True )

    class Meta:
        ordering = ('-created_at',)


class OrderItem(models.Model):
    order = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=20, null=True)
    price = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)



