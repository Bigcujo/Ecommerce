from .cart import Cart

# create a context processor so the cart can work on all pages.
def cart(request):
    return {'cart': Cart(request)}