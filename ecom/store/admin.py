from django.contrib import admin
from .models import Category, CustomUser, Product, Order, Profile
# Register your models here.
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


# Mix profile info and user info
class ProfileInLine(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = CustomUser
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInLine]

#Unregister the old way
admin.site.unregister(CustomUser)

#re-register the new way
admin.site.register(CustomUser, UserAdmin)
