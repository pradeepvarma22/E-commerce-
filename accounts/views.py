from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.shortcuts import render
from accounts.forms import AddProduct
from accounts.models import Seller
from ecomApp.models import Product
from django.urls import reverse_lazy
from django.contrib import messages 
from accounts.models import Customer


def HomeF(req):
    obj = Seller.objects.all()
    context ={
        'print' : obj
    }

    return render(req,'FirstPage.html',context)


def Clogin(request):

    if request.POST:

        if request.session['walletaddress']:
            del request.session['walletaddress']
        walletaddr = request.POST.get('address')
        tempobj=None
        request.session['walletaddress'] = walletaddr
        try:
            tempobj = Customer.objects.get(walletaddress=walletaddr)
        except:
            print('no user')
        if tempobj:
            return redirect('home')
        else:
            customer=Customer()
            customer.walletaddress =walletaddr 
            customer.save()
            print(walletaddr)
            return redirect('home')
    else:
        return render(request,'accounts/customer/login.html')
       

def Logout(req):
    return redirect('homef')

def Slogin(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        return redirect('sellerp')
    else:
        return redirect('slogin')


    return render(request,'accounts/seller/login.html')

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




def delete_product(req,pkk):
    obj = Product.objects.get(id=pkk)
    obj.delete()
    return redirect('sellerp')




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
