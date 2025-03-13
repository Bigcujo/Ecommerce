from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShippingAddress
from store.models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_shipping_address(sender, instance, created, **kwargs):
    if created:
        ShippingAddress.objects.get_or_create(user=instance)

