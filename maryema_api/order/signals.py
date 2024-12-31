from django.db.models import F, Sum, signals
from django.dispatch import receiver

from order.models import OrderItem


@receiver([signals.post_save, signals.post_delete], sender=OrderItem)
def update_order_total(sender, instance, created=False, **kwargs):
    """Updates the total of the order when an order item is created or updated or removed"""
    order = instance.order
    order.total = (
        order.items.annotate(
            subtotal=F("product_variant__price") * F("quantity")
        ).aggregate(Sum("subtotal"))["subtotal__sum"]
        or 0
    )
    order.save()
