from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
# Create your views here.


# cart summary view.
def cart_summary(request):
    return render(request, "cart/cart_summary.html", {})

# add to cart view.
def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # get product
        product_id = int(request.POST.get('product_id'))
        
        # lookup the product in DB
        product = get_object_or_404(Product, id=product_id)

        #save to session
        cart.add(product=product)

        # Get Cart Quantity
        cart_quantity = cart.__len__()


        # Return response
        #response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty': cart_quantity})
        return response
    

# delete cart view.
def cart_delete(request):
    pass

#  update cart view.
def cart_update(request):
    pass