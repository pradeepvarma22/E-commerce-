from django.db import models
from accounts.models import Seller

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(null=False,blank=True)
    createdon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


