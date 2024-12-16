from django.db.models import F, Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver

from cart.models import CartItem


@receiver([post_save, post_delete], sender=CartItem)
def update_cart_total(sender, instance, **kwargs):
    """Update the total of the cart"""
    active_cart = instance.cart
    active_cart.total = (
        CartItem.objects.filter(cart=active_cart)
        .annotate(subtotal=F("quantity") * F("product__price"))
        .aggregate(total_price=Sum("subtotal"))["total_price"]
    )
    active_cart.save()
