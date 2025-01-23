from django.shortcuts import render, redirect
from .models import Product, Category, CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ChangePasswordForm

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
            messages.success(request, f'Your account has been created successfully for {user_name}!!')
            form.save()
            return redirect('home')  # Redirect to login after successful registration
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
        current_user = CustomUser.objects.get(id=request.user.id)
        user_form = UserUpdateForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User has been Updated!!")
            return redirect('home')
        return render(request, "store/update_user.html", {'user_form':user_form})
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
                form = ChangePasswordForm(current_user)
                return render(request, 'store/update_password.html', {'form':form})
        else:
            messages.success(request, "You must be Logged in to access this page")
            return redirect('home')