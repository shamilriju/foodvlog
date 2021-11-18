from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from shamart import urls
from django.core.paginator import Paginator,EmptyPage,InvalidPage

from .models import *
# Create your views here.
#filter
def home(request,c_slug=None):
    c_page=None
    prodt=None
    if c_slug!=None:
        c_page=get_object_or_404(category,slug=c_slug)
        prodt=products.objects.filter(categ=c_page,available=True)
    else:
        prodt=products.objects.all().filter(available=True)
    cat=category.objects.all()
    #pagenumber
    paginator=Paginator(prodt,6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        pro=paginator.page(page)
    except(EmptyPage,InvalidPage):
        pro=paginator.page(paginator.num_pages)
    #pagenumberend
    return render(request,"home.html",{'ct':cat,'prod':prodt,'pg':pro})

def proddetails(request,c_slug,product_slug):
    try:
        prod=products.objects.get(categ__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'pr':prod})

def search(request):
    prod=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        prod=products.objects.all().filter(Q(name__contains=query)|Q(desc__contains=query))

    return render(request,'search.html',{'qr':query,'pr':prod})