from django.shortcuts import render,get_object_or_404,HttpResponse
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,Page
from django.db.models import Q
# Create your views here.
def store(request,category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        
        products = Product.objects.filter(category=categories,is_available=True).order_by('id')
        product_count = products.count()
        pagintor = Paginator(products,2)
        page_number = request.GET.get("page")
        page_obj = pagintor.get_page(page_number)
    else:
         products = Product.objects.all().filter(is_available=True).order_by('id')
         product_count = products.count()
         pagintor = Paginator(products,6)
         page_number = request.GET.get("page")
         page_obj = pagintor.get_page(page_number)
    context = {
        'products':page_obj,
        'count':product_count,

    }
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug=None):
    try:
        product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        is_cart = CartItem.objects.filter(cart__cart_id  = _cart_id(request),product=product).exists()
       
    except CartItem.DoesNotExist:
        pass
    context = {
        'is_cart':is_cart,
        'product':product,
       
    }
    
  
    return render(request,'store/product-detail.html',context)

def search(request):
    products = Product.objects.none()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
           products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).order_by('-created_date')
           product_count = products.count()

    context = {
            'products':products,
            'count':product_count
    }
        
  
    return render(request,'store/store.html',context)

