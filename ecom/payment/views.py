from django.shortcuts import render, redirect
from cart.cart import Cart
from .models import ShippingAddress
from .forms import ShippingForm, PaymentForm
from django.contrib import messages
from .models import Order, OrderItem
# Create your views here.
def checkout(request):
    #Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # checkout as logged in user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        return render(request, 'payment/checkout.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        # checkout as non logged user
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})


def payment_success(request):
    return render(request, 'payment/payment_success.html', {} )


#billing info page
def billing_info(request):
    if request.POST:
        #get cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        # create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        #check to see if user is logged in
        if request.user.is_authenticated:
            billing_info = PaymentForm()
            return render(request,  'payment/billing_info.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, 'billing_info':billing_info})
        else:
            billing_info = PaymentForm()
            return render(request,  'payment/billing_info.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, 'billing_info':billing_info})
        
        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

# process order
def process_order(request):
    if request.method == "POST":
        #get the cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # Get billing info from the last page
        payment_form = PaymentForm(request.POST or None)
        # get shipping Data
        my_shipping = request.session.get('my_shipping')
        if not my_shipping:
            messages.error(request, "Shipping information is missing. Please complete billing info first.")
            return redirect('payment/billing_info')


        #gather order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # create shipping Address from the session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        print("User:", request.user.username)
        print("Order Total:", amount_paid)
        print("Shipping Data:", my_shipping)


        #create an order model with the information gotten from the session
        if request.user.is_authenticated:
            #get the the logged in user
            user = request.user
            # create order
            print(user)
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            messages.success(request, "Order Placed")
            return redirect('home')
        else:
            #not logged in users
            #create new Order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            messages.success(request, "Order Placed")
            return redirect('home')
    else:
        messages.success(request, "Access Denied")
        return redirect('home')






