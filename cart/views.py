from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def cartdetails(request,tot=0,count=0,ct_items=None):
    try:
        ct=cartlist.objects.get(cart_id=c_id(request))
        ct_items=items.objects.filter(cart=ct,active=True)
        for i in ct_items:
            tot+=(i.prod.price*i.quantity)
            count+=i.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',{'t':tot,'cn':count,'ci':ct_items,})

def c_id(request):
    ct_id=request.session.session_key
    if not ct_id:
        ct_id=request.session.create()
    return ct_id

def add_cart(request,product_id):
    prod=products.objects.get(id=product_id)
    try:
        ct=cartlist.objects.get(cart_id=c_id(request))
    except cartlist.DoesNotExist:
        ct=cartlist.objects.create(cart_id=c_id(request))
        ct.save()
    try:
        c_items=items.objects.get(prod=prod,cart=ct)
        if c_items.quantity < c_items.prod.stock:
            c_items.quantity+=1
        c_items.save()
    except items.DoesNotExist:
        c_items=items.objects.create(prod=prod,quantity=1,cart=ct)
        c_items.save()
    return redirect('cartdetails')


def min_cart(request,product_id):
    ct=cartlist.objects.get(cart_id=c_id(request))
    prodt=get_object_or_404(products,id=product_id)
    c_items=items.objects.get(prod=prodt,cart=ct)
    if c_items.quantity>1:
        c_items.quantity-=1
        c_items.save()
    else:
        c_items.delete()
    return redirect('cartdetails')

def cart_delete(request,product_id):
    ct = cartlist.objects.get(cart_id=c_id(request))
    prodt = get_object_or_404(products,id= product_id)
    c_items = items.objects.get(prod=prodt, cart=ct)
    c_items.delete()
    return redirect('cartdetails')

