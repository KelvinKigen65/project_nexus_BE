from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer
from notifications.tasks import send_order_confirmation_email


class OrderListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .select_related('user')
            .prefetch_related('items__product')
            .order_by('-created_at')
        )
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Send confirmation email asynchronously
        send_order_confirmation_email.delay(order.id)

        headers = self.get_success_headers(serializer.data)
        return Response(
            OrderSerializer(order, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
