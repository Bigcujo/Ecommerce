from django.shortcuts import render

# Create your views here.


# cart summary view.
def cart_summary(request):
    return render(request, "cart/cart_summary.html", {})

# add to cart view.
def cart_add(request):
    pass

# delete cart view.
def cart_delete(request):
    pass

#  update cart view.
def cart_update(request):
    pass