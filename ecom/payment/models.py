from django.db import models
from store.models import CustomUser

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True )
    shipping_full_name = models.CharField(max_length=255)
    shipping_email= models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255)

    # don't pluralize address, this will show what is given below
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address = {str(self.id)}'