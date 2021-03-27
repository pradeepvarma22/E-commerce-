from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect
from django.views.generic import CreateView
from accounts.models import User
from accounts.form import CustomerSignUpForm,SellerSignUpForm
from django.shortcuts import render
from accounts.decorators import customer_required,seller_required
from django.contrib.auth.decorators import login_required
from accounts.forms import AddProduct


def HomeF(req):
    return render(req,'FirstPage.html')

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


def Clogin(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('clogin')


    return render(request,'accounts/customer/login.html')

def Logout(req):
    logout(req)
    return redirect('homef')

def Slogin(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('sellerp')
        else:
            return redirect(request, 'slogin')


    return render(request,'accounts/seller/login.html')



@login_required
@seller_required
def sellerV(req):
    obj =AddProduct
    if req.method=='POST':
        obj2 = AddProduct(req.POST)
        if obj2.is_valid():
            obj2.save()
    context={'obj_t':obj}
    return render(req,'accounts/seller/index.html',context)

