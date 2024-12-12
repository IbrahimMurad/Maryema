from django.db import models

from core.models import BaseModel
from stock.models import Stock
from users.models import Profile


class Cart(BaseModel):
    """Cart model"""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.BooleanField(
        default=True, help_text="True if cart is active, False if cart is inactive"
    )

    def __str__(self) -> str:
        return f"{self.profile}'s cart"

    class Meta:
        verbose_name_plural = "Carts"
        db_table = "cart"
        constraints = [
            models.UniqueConstraint(
                fields=["profile"],
                condition=models.Q(status=True),
                name="unique_active_cart",
            )
        ]


class CartItem(BaseModel):
    """CartItem model"""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product} x {self.quantity} in {self.cart}"

    @property
    def subtotal(self) -> float:
        return self.quantity - self.product.discount.amount
