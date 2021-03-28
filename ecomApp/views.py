from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import *
from accounts.decorators import customer_required,seller_required
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from ecomApp.forms import OrderForm


@login_required
@customer_required
def Home(request, itemname='all'):
    if itemname == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(desc=itemname)
    context = {
        'products': products
    }

    return render(request, 'ecomApp/home.html', context)


def page_view(request,id):
    obj = Product.objects.get(id=id)
    context = {'product':obj}
    return render(request,'ecomApp/product_page_view.html',context)


@login_required
@customer_required
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")

@login_required
@customer_required
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")

@login_required
@customer_required
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required
@customer_required
def item_decrement(request, id):
    cart = Cart(request)
    for pro in cart.session['cart'].values():
        quan = pro['quantity']
    if(quan==1):
        item_clear(request,id)

    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required
@customer_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required
@customer_required
def cart_detail(request):
    cart = Cart(request)
    dic = list(cart.session['cart'].values())
    total_price = sum([each['quantity']*(float(each['price'])) for each in dic])
    context = {"total":total_price}

    return render(request, 'ecomApp/cart.html',context)


def order(request):
    cart = Cart(request)
    dic = list(cart.session['cart'].values())
    total_price = sum([each['quantity'] * (float(each['price'])) for each in dic])

    if request.method == 'POST':
        mainuser = request.user
        customeruu = Customer.objects.get(user=mainuser)
        user = customeruu
        new_order = Checkout(user=user)
        form = OrderForm(request.POST, instance=new_order)
        if form.is_valid():
            order = form.save()
            print(cart.session['cart'].values())

            for prod in cart.session['cart'].values():
                OrderItem.objects.create(order=order,name=prod['name'],price=str(prod['price']),quantity=prod['quantity'])

            cart.clear()
            return redirect('home')

    form = OrderForm()
    context = {'form':form,
               'total_price':total_price
               }
    return render(request, 'ecomApp/order.html',context)
