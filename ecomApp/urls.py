from django.urls import path
from ecomApp.views import Home


urlpatterns = [
    path('',Home,name='home')
]