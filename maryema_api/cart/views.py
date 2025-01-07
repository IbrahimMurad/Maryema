from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerrializer, CartSerializer


class GetCartView(APIView):

    def get(self, request):
        """
        Retrieves the current user's current active cart
        """
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        cart = Cart.objects.get(customer=request.user.profile, is_active=True)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class ClearCartView(APIView):
    def delete(self, request):
        """
        Clears the current user's active cart
        """
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.profile.role != "customer":
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.user.profile.cart is None:
            new_cart = Cart.objects.create(
                customer=request.user.profile, is_active=True
            )
            serializer = CartSerializer(new_cart)
            return Response(serializer.data)
        cart = Cart.objects.get(customer=request.user.profile, is_active=True)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddToCartView(APIView):

    def post(self, request):
        """
        Adds an item to the current user's active cart
        """
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.profile.role != "customer":
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.user.profile.cart is None:
            cart = Cart.objects.create(customer=request.user.profile, is_active=True)
        else:
            cart = Cart.objects.get(customer=request.user.profile, is_active=True)
        serializer = CartItemSerrializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteCartItemView(APIView):

    def patch(self, request, pk):
        """
        Updates the quantity of a cart item
        """
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        cart_item = CartItem.objects.get(id=pk)
        if cart_item.cart.customer != request.user.profile:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CartItemSerrializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Deletes a cart item
        """
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        cart_item = CartItem.objects.get(id=pk)
        if cart_item.cart.customer != request.user.profile:
            return Response(status=status.HTTP_403_FORBIDDEN)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
