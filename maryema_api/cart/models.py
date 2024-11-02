from django.db import models

from core.models import BaseModel
from stock.models import Stock
from users.models import User


class Cart(BaseModel):
    """Cart model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.user}'s cart"


class CartItem(BaseModel):
    """CartItem model"""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.stock} x {self.quantity} in {self.cart}"

    @property
    def subtotal(self) -> float:
        return self.product.price_after_discount * self.quantity
