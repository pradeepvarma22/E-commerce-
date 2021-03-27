from django.urls import path
from ecomApp.views import *
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    path('home/',Home,name='home'),
    path('additem/<int:itemid>/', addCartV, name='additemtocart'),
    path('cart/', cartV, name='cart'),
    path('updateitem/<int:id>', UpdateItem, name='updateitem'),
    path('remove/<int:id>', remove_from_cart, name='removefromcart')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
