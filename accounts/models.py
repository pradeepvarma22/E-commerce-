from django.db import models




class Customer(models.Model):
    walletaddress = models.CharField(max_length=500,null=True,blank=True)

class Seller(models.Model):
    walletaddress = models.CharField(max_length=500,null=True,blank=True)