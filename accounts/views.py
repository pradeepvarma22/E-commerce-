from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from accounts.models import User
from accounts.form import CustomerSignUpForm,SellerSignUpForm
from django.shortcuts import render
from accounts.decorators import customer_required,seller_required
from django.contrib.auth.decorators import login_required
from accounts.forms import AddProduct
from accounts.models import Seller
from ecomApp.models import Product
from django.urls import reverse_lazy



def HomeF(req):
    obj = Seller.objects.all()
    context ={
        'print' : obj
    }

    return render(req,'FirstPage.html',context)

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
        return redirect('home')


class SellerSignUpView(FormView):
    model = User
    form_class = SellerSignUpForm
    template_name = 'accounts/seller/signup.html'
    success_url = reverse_lazy('sellerp')
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'seller'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return redirect('sellerp')
        else:
            return self.form_invalid(form)
    
    def form_invalid(self,form):
        form.add_error(None,"Password and userName should not same")
        return super(FormView,self).form_invalid(form)


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
def sellerV(request):
    obj =AddProduct
    mainuser = request.user
    suser = Seller.objects.get(user=mainuser)
    if request.POST:
        inss = Product(user=suser)
        form = AddProduct(request.POST,request.FILES,instance=inss)
        print(form)
        if form.is_valid():
            form.save()
        else:
            print('nooooooooooooooo')

    product_by_seller = Product.objects.filter(user=suser)
    context={'obj_t':obj,'sproducts':product_by_seller}

    return render(request,'accounts/seller/index.html',context)



 #
 #
 #
 # if req.method=='POST':
 #        form = AddProduct(req.POST)
 #        if form.is_valid():
 #            Product = form.save(commit=False)
 #            Product.seller=req.user
 #            Product.save()
 #            return redirect('sellerp')
 #
 #
 #
 #
 #
 #
 # product_name = req.POST.get('name')
 #        product_price = req.POST.get('price')
 #        product_image = req.POST.get('image')
 #        print('-------------------------------------------------------------------')
 #        print(product_image)
 #        print('----------------------------------------------------------')
 #        product_obj = Product(seller =product_seller_obj,name=product_name,price=product_price,image=product_image)
 #        product_obj.save()
 #        return redirect('sellerp')
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #
 #    sellerobj = Seller.objects.get(user=request.user)
 #    product_by_seller = Product.objects.filter(user=sellerobj)
 #    if request.method=='POST':
 #
 #        instance = Product(user=sellerobj)
 #
 #        form = AddProduct(instance=instance,data=request.POST)
 #
 #        if form.is_valid():
 #            print('Iiiiiiiiiiiiiiiiiiiiii    ammmmmmmmmm valid')
 #            form.save()
 #            return redirect('sellerp')
 #        else:
 #            print('pradepppppppppppppppppppppppppppppppppp')
