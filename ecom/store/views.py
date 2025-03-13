from django.shortcuts import render, redirect
from .models import Product, Category, CustomUser, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ChangePasswordForm, UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart
from payment.models import ShippingAddress
from payment.forms import ShippingForm
# Create your views here.


#category summary page
def category_summary(request):
    categories = Category.objects.all()

    return render(request, 'store/category_summary.html', {"categories":categories})


#category page
def category(request, boo):
    #swap the dash for space
    boo = boo.replace('-', ' ')
    # Grab the category from the url
    try:
        category = Category.objects.get(name=boo)
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html', {'products':products,  'category':category})
    except:
        messages.success(request, (" That Category Doesn't exist !!"))
        return redirect('home')




# product view 
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product.html', {'product':product})

# home view 
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products':products})

# about view
def about(request):
    return render(request, 'store/about.html', {})

# the login view
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #Do stuffs to the shopping cart
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)
                #add the loaded cart to the front-end
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, f"Welcome back {user.get_username()}")
            return redirect('home')
        else:
            messages.success(request, "Try again there was an issue trying to login")
            return redirect("login")
    else:
        return render(request, 'store/login.html', {})

# the logout view
def logout_view(request):
    logout(request)
    messages.success(request, (" You have been succesfully logged out!!....Thanks for shopping with us "))
    return redirect('home')


# the register view
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            messages.success(request, f'Your account has been created successfully for {user_name}!!')
            form.save()
            user = authenticate(username=user_name, password=password)
            login(request, user)
            return redirect('update_info')  # Redirect to login after successful registration
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        form = UserRegistrationForm()
        print("GET request")

    return render(request, 'store/register.html', {'form': form})


# the user update page
def update_user(request):
    if request.user.is_authenticated:
        #get curret user
        current_user = request.user
        print(current_user)
        # get curret user's shipping form
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        user_form = UserUpdateForm(request.POST or None, instance=current_user, prefix="user")
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user, prefix="shipping")
        

        if user_form.is_valid() or shipping_form.is_valid():
            user_form.save()
            shipping_form.save()
            login(request, request.user)
            messages.success(request, "User has been Updated!!")
            return redirect('home')
        return render(request, "store/update_user.html", {'user_form':user_form, 'shipping_form':shipping_form})
    else:
        messages.success(request, "You must be logged in To Access That Page!!")
        return  redirect('home')

# update user password
def update_password(request):
        if request.user.is_authenticated:
            current_user = request.user
            if request.method == 'POST':
                form = ChangePasswordForm(current_user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Your Password has been updated!!")
                    login(request, current_user)
                    return redirect('update_user')
                else:
                    for error in list(form.errors.values()):
                        messages.error(request, error)
                        return redirect('update_password')


            else:
                form = ChangePasswordForm(current_user)
                return render(request, 'store/update_password.html', {'form':form})
        else:
            messages.success(request, "You must be Logged in to access this page")
            return redirect('home')
        


# update user info
def update_info(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid():
            # save userinfo form
            form.save()
            messages.success(request, "Your Info has been Updated")
            return redirect('home')
        return render(request, "store/update_info.html", {'form':form})
    else:
        messages.success(request, "You Must Be logged In To Access That Page!!")
        return redirect('home')
    

# search view
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched) )
        if not searched:
            messages.success(request, "Searched item not availabe")
        return render(request, 'store/search.html', {'searched':searched})
    return render(request, 'store/search.html', {})