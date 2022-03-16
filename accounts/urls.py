from django.urls import path,include
from accounts.views import sellerV,Clogin,Slogin,Logout,HomeF,delete_product,HomeSeller
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('',HomeF,name='homef'),
    path('SellerP/<str:addr>/',HomeSeller,name='homes'),
    path('logout/',Logout,name='logout'),
    path('clogin/',Clogin,name='clogin'),
    path('slogin/',Slogin,name='slogin'),
    path('sellerpage/<str:addr>/',sellerV,name='sellerp'),
    path('delete_product/<str:pkk>/',delete_product,name='delete_product')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
