from django.shortcuts import render, get_object_or_404,redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.


# cart summary view.
def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart/cart_summary.html", {"cart_products": cart_products, "quantities": quantities, 'totals': totals})

# add to cart view.
def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # get product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        # lookup the product in DB
        product = get_object_or_404(Product, id=product_id)

        #save to session
        cart.add(product=product, quantity =product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()


        # Return response
        #response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, (" Product added to cart !!"))
        return response
    

# delete cart view.
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get product
        product_id = int(request.POST.get('product_id'))
        # call the delete function in Cart
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
        messages.success(request, (" Product removed from cart !!"))
        return response
        #return redirect('cart_summary')

#  update cart view.
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # get product
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
    
        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request, (" Cart updated !!"))
        return response
        #return redirect('cart_summary')