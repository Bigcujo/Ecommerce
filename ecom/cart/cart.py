from store.models import Product

class Cart():
    # init method
    def __init__(self, request):
        self.session = request.session

        #Get the current user's session key if it exists
        cart = self.session.get('session_key')

        # if the user is new, then no session key so we create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of the site
        self.cart = cart
    # add method for the cart
    def add(self, product):
        product_id = str(product.id)

        # Logic to add to cart
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True
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
