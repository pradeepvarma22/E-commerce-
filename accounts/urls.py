from django.urls import path
from accounts.views import CustomerSignUpView,customerV,SellerSignUpView,sellerV

urlpatterns = [
    path('csignup/',CustomerSignUpView.as_view(),name='csignup'),
    path('ssignup/',SellerSignUpView.as_view(),name='ssignup'),
    path('customerpage/',customerV,name='customerp'),
    path('sellerpage/',sellerV,name='sellerp')
]
