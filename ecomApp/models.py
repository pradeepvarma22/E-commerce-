from django.db import models
from accounts.models import Seller




class Product(models.Model):
    user = models.ForeignKey(Seller,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


