from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import *
from cart.cart import Cart
from ecomApp.forms import OrderForm,RatingForm
from django.db.models import Case, When
from django.core.exceptions import ObjectDoesNotExist



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
    ratingform = RatingForm
    rating_ = MyRating.objects.filter(product=Product.objects.get(id=id))
    sum=0
    cou = 0
    for i in rating_:
        sum = sum + int(i.rating)
        cou =cou+1
    
    avg_rating=0
    try:
        avg_rating = sum/cou
    except:
        avg_rating = 0
    
    mainuser = request.user
    customeruu = Customer.objects.get(user=mainuser)
    user = customeruu
    if request.method=='POST':
        
        form = RatingForm(request.POST)
        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.user = user
            new_obj.product=Product.objects.get(id=id)
            new_obj.save()
            return redirect('page_view',id)


    obj = Product.objects.get(id=id)
    Flagg = False
    valuee=0
    try:
        test_=MyRating.objects.get(user=user,product=obj)
    except ObjectDoesNotExist:
        test_ = None

    
    if test_ is not None:
        Flagg = True

    if test_ is None:
        Flagg = False

    context = {'product':obj,'ratingform':ratingform,'rateduser':Flagg,'rating':avg_rating}
    return render(request,'ecomApp/product_page_view.html',context)


def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    addr = request.session['walletaddress']
    return redirect("homes",addr)

def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")

def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

def item_decrement(request, id):
    cart = Cart(request)
    for pro in cart.session['cart'].values():
        quan = pro['quantity']
    if(quan==1):
        item_clear(request,id)

    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

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
        mainuser = request.session['walletaddress']
        customeruu = Customer.objects.get(walletaddress=mainuser)
        user = customeruu
        new_order = Checkout(user=user)
        form = OrderForm(request.POST, instance=new_order)
        if form.is_valid():
            order = form.save()
            print(cart.session['cart'].values())

            for prod in cart.session['cart'].values():
                OrderItem.objects.create(order=order,name=prod['name'],price=str(prod['price']),quantity=prod['quantity'])

            cart.clear()
            addr = request.session['walletaddress']
            return redirect('homes',addr)

    form = OrderForm()
    context = {'form':form,
               'total_price':total_price
               }
    return render(request, 'ecomApp/order.html',context)





# To get similar Products based on user rating
def get_similar(product_name,rating,corrMatrix):
    similar_ratings = corrMatrix[product_name]*(rating-2)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings
