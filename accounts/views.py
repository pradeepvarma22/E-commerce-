from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from accounts.models import User
from accounts.form import CustomerSignUpForm,SellerSignUpForm
from django.shortcuts import render
from accounts.decorators import customer_required,seller_required
from django.contrib.auth.decorators import login_required



class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'accounts/customer/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customerp')


class SellerSignUpView(CreateView):
    model = User
    form_class = SellerSignUpForm
    template_name = 'accounts/seller/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'seller'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('sellerp')


@login_required
@customer_required
def customerV(req):
    return render(req,'accounts/customer/index.html')


@login_required
@seller_required
def sellerV(req):
    return render(req,'accounts/seller/index.html')

