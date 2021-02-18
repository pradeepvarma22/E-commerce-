from django.contrib import admin
from accounts.models import User,Customer,Seller

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Seller)
