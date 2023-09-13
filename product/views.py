from django.shortcuts import render , redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Items, Cart
from .forms import CustomerRegistrationForm, CustomerProfileForm ,Customer
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.db.models import Q

# Create your views here.
def test(request):
    return render(request,"test.html")
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")
class CategoryView(View):
    def get(self,request,val):
        product = Items.objects.filter(category = val)
        title = Items.objects.filter(category = val).values('title')
        return render(request,"category.html",locals())
class ProductDetail(View):
    def get(self,request,pk):
        product = Items.objects.get(pk = pk)
        return render(request,"detail.html",locals())
def checkout(request):
    return render(request,"checkout.html")
def contact(request):
    return render(request,"contact.html")
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,"signup.html",locals())
    def post(self,request):
        form =CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Successful")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, "signup.html", locals())
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'profile.html',locals())
def add_to_cart(request):
    user = request.user
    product_id =  request.GET.get('prod_id')
    quantity = int(request.GET.get('quantity',1))
    product = get_object_or_404(Items,id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=user,product=product)
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('/cart')


def add_to_cart_new(request):
    if request.method == 'POST':
        user = request.user
        quantity = 1
        product_id = request.POST.get('prod_id')
        cart_item, created = Cart.objects.get_or_create(user=user)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
    return redirect('/cart')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discount_price
        amount = amount+value
    totalamount = amount + 40
    return render(request,'addtocart.html',locals())
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        totalamount = amount +40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        if c.quantity <= 0:
            c.delete()  # Delete the item if quantity becomes 0 or negative
        else:
            c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        totalamount = amount +40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        totalamount = amount + 40.0
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def address(request):
    add = Customer.objects.filter(user =request.user )
    return render(request,"address.html",locals())
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,"update-address.html",locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Profile Updated!!")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
