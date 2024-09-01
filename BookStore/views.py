from django.shortcuts import render,HttpResponse,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from subscribe.views import subscribe_func,subscribe_second_func
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import date as dt

# Create your views here.
def index(request):
    labels = []
    data = []

    queryset = Statistic.objects.order_by('-count')[:6]
    sum = 0

    for i in queryset:
        labels.append(i.name)
        data.append(i.count)
        sum = sum + i.count

    news = News.objects.order_by('-created')
    partners = Partners.objects.all()
    context = {
        'News':news,
        'Partners':partners,
        'labels': labels,
        'data': data,
        'sum': sum,
    }
    return render(request, 'index.html', context)

def contact(request):
    return render(request, 'contact.html')

def ourteam(request):
    return render(request, 'ourteam.html')

def partner(request):
    partner = Partners.objects.all()
    context = {'partner':partner}
    return render(request, 'partners.html', context)

def shop(request):
    cart=request.session.get('cart')
    if not cart:
        request.session.cart = {}
    category = Category.objects.all()
    Featured = FeaturedProduct.objects.all()
    hoodie = Product.objects.all()
    print(Featured)
    context = {
        'Featured':Featured,
        'Hoodie':hoodie,
        'category':category,
        'Cart':'Cart is empty',
    }
    return render(request, 'ecom.html', context)
    

def product(request,id):
    cart=request.session.get('cart')
    if not cart:
        request.session.cart = {}
    product = get_object_or_404(Product, id=id)
    context = {
        'Product':product,
    }
    # request.session.get('cart').clear()
    return render(request, 'product.html', context)

def cart(request):
    cart=request.session.get('cart')
    if not cart:
        request.session.cart = {}
    product = request.POST.get('product_id')
    removeProduct=request.POST.get('removeProduct')
    if cart:
        quantity = cart.get(product)
        if quantity:
            if removeProduct:
                if quantity==1:
                    cart.pop(product)
                else:
                    cart[product] = quantity-1
            else:
                cart[product] = quantity+1
        else:
            cart[product] = 1
    else:
        cart = {}
        cart[product] = 1
    request.session['cart'] = cart
    return redirect(request.META['HTTP_REFERER'])

def cartProducts(request):
    cart = request.session.get('cart', {})
    if not cart:
        empty_msg = "Your cart is empty."
        return render(request, 'cartProducts.html', {'empty_msg': empty_msg})
    ids = list(cart.keys())
    products_in_cart = Product.getProductByID(ids)
    orders = order.objects.all()
    context = {
        'Cart': products_in_cart,
        'Order': orders,
    }
    return render(request, 'cartProducts.html', context)

def loginCheckout(request):
    if request.user.is_authenticated:
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        readAndReturn=request.POST.get('readAndReturn') == 'on'
        returnDate_str = request.POST.get("returnDate")
        cart = request.session.get('cart')
        products = Product.getProductByID(list(cart.keys()))
        customer = (request.user.id)
        print(returnDate_str)
        print(returnDate_str)
        print(returnDate_str)
        print(returnDate_str)

        if not returnDate_str:
            print('12345')
            returnDate = None
        else:
            returnDate = returnDate_str


        for i in products:
            Order=order(Customer=User(id=customer),
                        product=i,
                        price=i.productPrice,
                        quantity=cart.get(str(i.id)),
                        address=address,
                        phone=phone,
                        readAndReturn=readAndReturn,
                        returnDate=returnDate)
            Order.placeOrder()
        request.session['cart']={}
        return redirect('/orders')
    else:
        return redirect('Signin')
    
def remove_from_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        for key in request.POST.keys():
            if key.isdigit():
                product_id = int(key)
                if str(product_id) in cart:
                    del cart[str(product_id)]  # Remove the item from the cart
        request.session['cart'] = cart
    return redirect('cartProducts')

def cartFinalRemove(request):
    product = request.POST.get('product_idd')
    cart = request.session['cart']
    cart.pop(product)
    # return redirect(request.META['HTTP_REFERER'])
    return redirect('cartProducts')

@login_required
def finalOrder(request):
    customer=request.user
    orders = order.objects.filter(Customer=customer)
    context = {
        'orders':orders,
    }
    return render(request, 'order.html', context)

def aboutus(request):
    return render(request, 'aboutus.html')

def ticketbooking(request):
    date = dt.today()
    if request.user.is_authenticated:
        context = {'form': BookTicket(), 'date':date}
        return render(request, 'ticketbooking.html', context)
    else:
        return redirect('Signin')

@login_required 
def booked(request):
    if request.method == 'POST':
        form = BookTicket(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return thankyou(request,'for booking! Your tickets will be sent to your email!') 
        else:
            return redirect('home')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        Email = request.POST['email']   
        if User.objects.filter(email=Email).exists():
            return render(request, 'signup.html', {'error':'Email already exists'})
        else: 
            try:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password1'])
                subscribe_func(request, Email)
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {'error':'User already exists'})
        
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        user = authenticate(request, username = request.POST['uname'], password = request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'error':'Invalid Username/Password'})
        else:
            login(request, user)
            return redirect('home') 

def logoutuser(request):
    cart=request.session.get('cart')
    if not cart:
        request.session.cart = {}
    logout(request)
    return redirect('home')

def blogs(request):
    Blog = blog.objects.all()
    latest = blog.objects.order_by('-created')
    context = {'Blog': Blog,'latest':latest}
    return render(request, 'blogpost.html', context)

def donate(request):
    if request.method == 'GET':
        return render(request, 'donate.html')
    else:
        donate = Donate.objects.create(fname = request.POST['fname'], lname = request.POST['lname'], phone = request.POST['phone'], email = request.POST['email'], address = request.POST['address'], comment = request.POST['comment'], amount = request.POST['amount'])
        donate.save()
        str = 'for donating!'
        return thankyou(request,str) 
        
def readblogs(request,id):
    Blog = get_object_or_404(blog,id=id)
    user = request.user
    if user.is_authenticated:
         return render(request, 'readblogs.html', {'Blog':Blog})
    else:
        return redirect('Signin')

def news(request):
    latest = News.objects.order_by('-created')
    news = News.objects.all()
    Category = NewsCategory.objects.all()
    context = {'News':news, 'Category':Category, 'latest':latest}
    return render(request, 'news.html', context)

def readnews(request,id):
    Newss = get_object_or_404(News, id=id)
    user = request.user
    return render(request, 'readnews.html', {'Newss':Newss})

def newscategory(request,id):
    news = get_object_or_404(NewsCategory,id=id)
    category = News.objects.filter(Category=news)
    context={'category':category}
    return render(request, 'newscategory.html', context)

def savecontact(request):
    if request.method == 'GET':
        return render(request, 'contact.html')
    else:
        user = Contact.objects.create(name = request.POST['name'], email= request.POST['email'], subject=request.POST['subject'], message=request.POST['message'])
        user.save()
        return thankyou(request,'for contacting us! We\'ll get in touch soon!')

def subscribeEmail(request):
    if request.method == 'POST':
        subEmail = request.POST.get('sub-email')
        subscribe_second_func(request,subEmail)
    return thankyou(request,'for subscribing us!')

def search(request):
    if request.method == 'GET':
        v = request.GET.get('value')
        news = News.objects.filter(newsTitle__contains = v)
        Empty = False
        if not news.exists():
            Empty = True
        context = {
            'news':news,
            'Title1':'News',
            'empty': Empty
        }
    else:   
        v = request.POST.get('value')
        product = Product.objects.filter(productTitle__contains = v)
        Empty = False
        if not product.exists():
            Empty = True
        context = {
            'product':product,
            'Title3':'Products',
            'empty': Empty
        }
    return render(request, 'search.html', context) 

def thankyou(request,str):
    context = {'str':str}
    return render(request, 'thankyou.html', context)

def pie_chart(request):
    labels = []
    data = []

    queryset = Statistic.objects.order_by('-count')[:6]
    sum = 0

    for i in queryset:
        labels.append(i.name)
        data.append(i.count)
        sum = sum + i.count

    return render(request, 'pie_chart.html', {
        'labels': labels,
        'data': data,
        'sum': sum,
    })