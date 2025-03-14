from store.models import Product, Profile

class Cart():
    # init method
    def __init__(self, request):
        self.session = request.session
        self.request = request

        #Get the current user's session key if it exists
        cart = self.session.get('session_key')

        # if the user is new, then no session key so we create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of the site
        self.cart = cart
    

    #add from the database.
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        #logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        #deal with logged in user
        if self.request.user.is_authenticated:
            # get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))



    #delete from the database
            


    # add method for the cart
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # Logic to add to cart
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        #deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            print(carty)
            current_user.update(old_cart=carty)

    # get the number of items in the shopping cart
    def __len__(self):
        return len(self.cart)
    
    # display the products in the shopping cart
    def get_prods(self):
        # get the ids from cart
        product_ids = self.cart.keys()
        
        #use ids to lookup the products in the database model
        products = Product.objects.filter(id__in=product_ids)
        # Return those looked up products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        #get cart
        ourcart = self.cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        
        if self.request.user.is_authenticated:
            # get cureent user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", ("\""))
            current_user.update(old_cart=str(carty))
        thing = self.cart
        return thing
    
    def delete(self,product):
        #grab the product id
        product_id = str(product)
        #delete from cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        if self.request.user.is_authenticated:
            # get cureent user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", ("\""))
            current_user.update(old_cart=str(carty))


    def cart_total(self):
        # getting all the keys in the cart dictioanry 
        product_ids = self.cart.keys()
        # use the product id in the cart to find the object in the database
        products = Product.objects.filter(id__in = product_ids)
        quantities = self.cart
        #start counting from zero
        total = 0
        #loop through the items in the dictionary 
        for key, value in quantities.items():
            # convert the key to an int so i can do 
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total



