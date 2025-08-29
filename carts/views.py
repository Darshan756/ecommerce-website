from django.shortcuts import render,HttpResponse,redirect
from store.models import Product,Variantions
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.
def _cart_id(request):
     cart = request.session.session_key
     if not cart:
          cart = request.session.create()
     return cart
def add_cart(request,product_id):
    
    product = Product.objects.get(id=product_id)
    product_variations = []
    if request.method == 'POST':
        for item in request.POST:
            if item == 'csrfmiddlewaretoken':
                continue
            key = item
            value = request.POST[key]
            try:
                variation = Variantions.objects.get(product=product,variation_categories__iexact=key,variation_value__iexact=value)
                product_variations.append(variation)
            except:
                pass

    
    try:
        if request.user.is_authenticated:
           cart = Cart.objects.get(user=request.user)
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        if request.user.is_authenticated:
           cart = Cart.objects.create(user=request.user)
        else:
           cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    
    
    is_cart_item_exits = CartItem.objects.filter(product=product,cart=cart).exists()
    if is_cart_item_exits:
        cart_item = CartItem.objects.filter(product=product,cart=cart)
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variation.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        if product_variations in ex_var_list:
            index = ex_var_list.index(product_variations)
            item_id = id[index]
            item = CartItem.objects.get(product=product,cart=cart,id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product,cart=cart,quantity=1)
            if len(product_variations) > 0:
                item.variation.clear()
                item.variation.add(*product_variations)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity = 1,
           

        )
        if len(product_variations) > 0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variations)
        cart_item.save()
    

    return redirect('cart')


def decrease_cart_item(request,cart_item_id):

    try:
        if request.user.is_authenticated:
           cart = Cart.objects.get(user=request.user)
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        return redirect('cart')

    try:
        cart_item = CartItem.objects.get(id=cart_item_id,cart=cart)
        if cart_item.quantity > 1 :
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')

def remove_cart(request,cart_item_id):
    try:
        if request.user.is_authenticated:
           cart = Cart.objects.get(user=request.user)
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        return redirect('cart')

    try:
        cart_item = CartItem.objects.get(id = cart_item_id,cart=cart)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')

def cart(request,total=0,quantity=0,cart_items=None):
    tax=0
    grand_total=0
    try:
        if request.user.is_authenticated:
           cart = Cart.objects.get(user=request.user)
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = total * 2
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context ={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'carts/cart.html',context)

@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    tax=0
    grand_total=0
    try:
        if request.user.is_authenticated:
           cart = Cart.objects.get(user=request.user)
        else:
           cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = total * 2
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context ={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request, 'carts/checkout.html',context)