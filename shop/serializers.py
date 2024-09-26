from rest_framework import serializers
from .models import Product, Cart, Order, OrderItem, CartItem, User

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)  

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups']
        
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField() 

    class Meta:
        model = Product
        exclude = ['id']
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        read_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'total_price']  

    def get_total_price(self, obj): 
        return obj.get_total_item_price()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True) 

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'items']