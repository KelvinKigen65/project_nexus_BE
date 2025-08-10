import stripe
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from .serializers import PaymentSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        try:
            order = Order.objects.get(pk=order_id, user=request.user)
            
            if order.status != Order.PENDING:
                return Response(
                    {'error': 'Order is already processed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            payment_intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),  # Convert to cents
                currency='usd',
                metadata={'order_id': order.id},
            )
            
            return Response({
                'clientSecret': payment_intent['client_secret'],
                'amount': order.total_price,
                'currency': 'usd'
            })
            
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class PaymentWebhookView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            handle_payment_success(payment_intent)

        return Response(status=status.HTTP_200_OK)

def handle_payment_success(payment_intent):
    order_id = payment_intent['metadata']['order_id']
    order = Order.objects.get(pk=order_id)
    order.status = Order.COMPLETED
    order.transaction_id = payment_intent['id']
    order.save()
    
    Payment.objects.create(
        order=order,
        user=order.user,
        amount=payment_intent['amount'] / 100,
        payment_intent_id=payment_intent['id'],
        status='succeeded'
    )