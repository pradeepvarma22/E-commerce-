from django.urls import path,include
from accounts.views import CustomerSignUpView,SellerSignUpView,sellerV,Clogin,Slogin,Logout,HomeF
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('',HomeF,name='homef'),
    path('logout/',Logout,name='logout'),
    path('clogin/',Clogin,name='clogin'),
    path('slogin/',Slogin,name='slogin'),
    path('csignup/',CustomerSignUpView.as_view(),name='csignup'),
    path('ssignup/',SellerSignUpView.as_view(),name='ssignup'),
    path('sellerpage/',sellerV,name='sellerp'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
