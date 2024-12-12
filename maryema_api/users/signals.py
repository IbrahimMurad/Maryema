from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from cart.models import Cart
from users.models import Profile


@receiver(post_save, sender=Profile)
def create_cart(sender, instance, created, **kwargs):
    if created:
        print(f"Profile created with role: {instance.role}")  # Debugging statement
        if instance.role == Profile.RoleChoices.CUSTOMER:
            Cart.objects.create(profile=instance, status=True)
            print("Cart created")  # Debugging statement
