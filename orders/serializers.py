from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from cart.serializers import CartSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'status_display', 'total_price', 'created_at', 
                 'updated_at', 'shipping_address', 'payment_method', 'transaction_id', 'items']

class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
    payment_method = serializers.CharField()

    def create(self, validated_data):
        request = self.context.get('request')
        cart = request.user.cart
        
        if not cart.items.exists():
            raise serializers.ValidationError("Cart is empty")
        
        order = Order.objects.create(
            user=request.user,
            shipping_address=validated_data['shipping_address'],
            payment_method=validated_data['payment_method'],
            total_price=cart.total_price
        )
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        cart.items.all().delete()
        return order