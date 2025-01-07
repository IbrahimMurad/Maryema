from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer


class BaseCartView(APIView):

    def get_cart(self, user):
        try:
            return Cart.objects.get(customer=user.profile, is_active=True)
        except Cart.DoesNotExist:
            return None

    def check_authentication(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return None

    def check_customer_role(self, request):
        if not request.user.profile.is_customer:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return None


class GetCartView(BaseCartView):

    def get(self, request):
        """
        Retrieves the current user's current active cart
        """
        auth_response = self.check_authentication(request)
        if auth_response:
            return auth_response

        cart = self.get_cart(request.user)
        if not cart:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class ClearCartView(BaseCartView):

    def delete(self, request):
        """
        Clears the current user's active cart
        """
        auth_response = self.check_authentication(request)
        if auth_response:
            return auth_response

        role_response = self.check_customer_role(request)
        if role_response:
            return role_response

        cart = self.get_cart(request.user)
        if not cart:
            cart = Cart.objects.create(customer=request.user.profile, is_active=True)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddToCartView(BaseCartView):

    def post(self, request):
        """
        Adds an item to the current user's active cart
        """
        auth_response = self.check_authentication(request)
        if auth_response:
            return auth_response

        role_response = self.check_customer_role(request)
        if role_response:
            return role_response

        cart = self.get_cart(request.user)
        if not cart:
            cart = Cart.objects.create(customer=request.user.profile, is_active=True)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteCartItemView(BaseCartView):

    def patch(self, request, pk):
        """
        Updates the quantity of a cart item
        """
        auth_response = self.check_authentication(request)
        if auth_response:
            return auth_response

        try:
            cart_item = CartItem.objects.get(id=pk)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if cart_item.cart.customer != request.user.profile:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Deletes a cart item
        """
        auth_response = self.check_authentication(request)
        if auth_response:
            return auth_response

        try:
            cart_item = CartItem.objects.get(id=pk)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if cart_item.cart.customer != request.user.profile:
            return Response(status=status.HTTP_403_FORBIDDEN)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
