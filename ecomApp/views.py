from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import *
from accounts.decorators import customer_required,seller_required
from django.contrib.auth.decorators import login_required




def cartV(request):
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id
        new_cart.save()

    if the_id:
        try:
            cartobj = Cart.objects.get(id=the_id)
            cartobj.save()
            context = {'cart': cartobj}
        except:
            request.session['items_count'] = 0
            context = {'empty': True}

    else:
        cart = None
        context = {'empty': True}

    return render(request, 'ecomApp/cart.html', context)



def remove_from_cart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        pass
    cartitem = CartItem.objects.get(id=id)
    cartitem.cart = None
    cartitem.save()
    return redirect('cart')

def UpdateItem(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        pass

    if request.method == 'POST':
        if request.POST.get('qty'):
            cartitem = CartItem.objects.get(item__id=id)
            qqty = request.POST.get('qty')
            cartitem.quantity = qqty
            cartitem.save()
    else:
        print('POST Not Working')
    return redirect('cart')


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


def addCartV(request, itemid):
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    try:
        cartobj = Cart.objects.all().get(id=the_id)
    except:
        cartobj = Cart()
        cartobj.id = the_id
        cartobj.save()

    itemobj = Product.objects.get(id=itemid)

    cart_item, created = CartItem.objects.get_or_create(cart=cartobj, item=itemobj)

    if created:
        new_total = 0
        for i in cartobj.cartitem_set.all():
            new_total = new_total + (i.item.product_price)
        cartobj.total = new_total
        request.session['items_count'] = cartobj.cartitem_set.count()
        cartobj.save()

    return redirect('home')
