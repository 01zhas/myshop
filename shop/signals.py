from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cart, Product, АvailabilityAlert

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
        instance.cart.save()


@receiver(pre_save, sender=Product)
def availability_alert(sender, instance, **kwargs):
    prod = sender.objects.filter(name = instance.name)[0]
    if prod.quantity == 0 and prod.quantity < instance.quantity:
        alerts = АvailabilityAlert.objects.filter(product = instance)
        for alert in alerts:
            print(alert)
            alert.delete()
            