from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import *
from accounts.decorators import customer_required,seller_required
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from ecomApp.forms import OrderForm,RatingForm
from django.db.models import Case, When
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist



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





# To get similar Products based on user rating
def get_similar(product_name,rating,corrMatrix):
    similar_ratings = corrMatrix[product_name]*(rating-2)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings

# Recommendation Algorithm
def recommend(request):
    
    product_rating=pd.DataFrame(list(MyRating.objects.all().values()))

    new_user=product_rating.user_id.unique().shape[0]
    mainuser = request.user
    customeruu = Customer.objects.get(user=mainuser)
    current_user_id= customeruu.user.id

	# if new user not rated any Product
    if current_user_id>new_user:
        product=Product.objects.first()   #Any object
        q=MyRating(user=customeruu,product=product,rating=1)
        q.save()

    #product_rating['rating']=pd.to_numeric(product_rating)
    convert_dict = {'rating': int } 
    product_rating = product_rating.astype(convert_dict)
    print(product_rating)
    print(product_rating.dtypes)
    userRatings = product_rating.pivot_table(index=['user_id'],columns=['product_id'],values='rating')
    userRatings = userRatings.fillna(0,axis=1)
    corrMatrix = userRatings.corr(method='pearson')

    user = pd.DataFrame(list(MyRating.objects.filter(user=customeruu).values())).drop(['user_id','id'],axis=1)
    user_filtered = [tuple(x) for x in user.values]
    product_id_watched = [each[0] for each in user_filtered]

    similar_products = pd.DataFrame()
    for product,rating in user_filtered:
        similar_products = similar_products.append(get_similar(product,int(rating),corrMatrix),ignore_index = True)

    products_id = list(similar_products.sum().sort_values(ascending=False).index)
    products_id_recommend = [each for each in products_id if each not in product_id_watched]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(products_id_recommend)])
    product_list=list(Product.objects.filter(id__in = products_id_recommend).order_by(preserved)[:10])

    context = {'product_list': product_list}
    return render(request, 'ecomApp/recommend.html', context)
