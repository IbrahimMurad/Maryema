from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
from core.permissions import IsCustomer
from order.models import Order, OrderItem
from order.serializers import OrderSerializer


class GetCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves the current user's current active cart.

        If there is no active cart, a new one is created
        """

        cart, created = Cart.objects.get_or_create(
            customer=request.user.profile, is_active=True
        )
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class ClearCartView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def delete(self, request):
        """
        Clears the current user's active cart.

        If there is no active cart, a new one is created which will be already empty
        """

        cart = Cart.objects.get_or_create(customer=request.user.profile, is_active=True)
        if cart.items.count() > 0:
            cart.items.all().delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        """
        Adds an item to the current user's active cart.

        If there is no active cart, a new one is created and add the item to it.
        """
        cart = Cart.objects.get_or_create(customer=request.user.profile, is_active=True)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteCartItemView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_cart_item(self, pk, request):
        """
        Retrieves a cart item by its id and checks if it belongs to the current user
        """
        try:
            cart_item = CartItem.objects.get(id=pk)
        except CartItem.DoesNotExist:
            return None, Response(status=status.HTTP_404_NOT_FOUND)

        if cart_item.cart.customer != request.user.profile:
            return None, Response(status=status.HTTP_403_FORBIDDEN)

        return cart_item, None

    def patch(self, request, pk):
        """
        Updates the quantity of a cart item
        """

        # Get cart item or 404
        # Also, check if the cart item belongs to the current user or 403
        cart_item, response = self.get_cart_item(pk, request)
        if response:
            return response

        # Update the cart item or 400 (bad request)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Deletes a cart item
        """

        # Get cart item or 404
        # Also, check if the cart item belongs to the current user or 403
        cart_item, response = self.get_cart_item(pk, request)
        if response:
            return response

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        """
        Checks out the current user's active cart
        """

        # Get the current user's active cart or create a new one if there is none
        # return 400 if the cart is empty (or created just now)
        cart, created = Cart.objects.get_or_create(
            customer=request.user.profile, is_active=True
        )
        if created or cart.items.count() == 0:
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create the order from the cart and return the order details
        try:
            order = Order.objects.create(customer=request.user.profile)
            items = cart.items.values("product_variant", "quantity")
            OrderItem.objects.bulk_create(
                [OrderItem(order=order, **item) for item in items]
            )
            order.total = cart.cost
            order.save()
            serializer = OrderSerializer(order)

            # deactivate the current cart and create a new one
            cart.is_active = False
            cart.save()
            Cart.objects.create(customer=request.user.profile, is_active=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            # handle ValueError specifically
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            # handle ValidationError specifically
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # handle any other exceptions
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
