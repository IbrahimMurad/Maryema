from rest_framework import status, viewsets
from rest_framework.response import Response

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer


class CartViewSet(viewsets.GenericViewSet):
    """Cart view set"""

    def get_queryset(self):
        """Return the active cart of the current user"""
        return Cart.objects.filter(profile=self.request.user.profile, status=True)

    def get_serializer_class(self):
        """Return the serializer class"""
        if self.action == "list":
            return CartSerializer
        return CartItemSerializer

    def list(self, request, *args, **kwargs):
        """retrieve the active cart of the current user"""
        active_cart = Cart.objects.get(profile=request.user.profile, status=True)
        serializer = self.get_serializer(active_cart)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a product from the active cart"""
        cart_item = CartItem.objects.get(id=kwargs["pk"])
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Add a product to the active cart"""
        active_cart = Cart.objects.get(profile=request.user.profile, status=True)
        quantity = int(request.data["quantity"]) if request.data["quantity"] else 1
        if active_cart.items.filter(product=request.data["product"]).exists():
            cart_item = active_cart.items.get(product=request.data["product"])
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                cart=active_cart,
                product_id=request.data["product"],
                quantity=quantity,
            )
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update the quantity of a product in the active cart"""
        cart_item = CartItem.objects.get(id=kwargs["pk"])
        cart_item.quantity = request.data["quantity"]
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Remove a product from the active cart"""
        cart_item = CartItem.objects.get(id=kwargs["pk"])
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
