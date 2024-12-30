from profile.models import Profile

from django.db.models import F, Sum, signals
from django.dispatch import receiver

from cart.models import Cart, CartItem


@receiver(signals.post_save, sender=Profile)
def create_cart(sender, instance, created, **kwargs):
    """Creates a cart for a new customer"""
    if created and instance.is_customer:
        Cart.objects.create(customer=instance)


@receiver([signals.post_save, signals.post_delete], sender=CartItem)
def update_cart_cost(sender, instance, created=False, **kwargs):
    """Updates the cost of the cart when a cart item is created or updated or removed"""
    cart = instance.cart
    cart.cost = (
        cart.items.annotate(
            subtotal=F("product_variant__price") * F("quantity")
        ).aggregate(Sum("subtotal"))["subtotal__sum"]
        or 0
    )
    cart.save()
