from django.urls import path
from .views import CreatePaymentIntentView, PaymentWebhookView

urlpatterns = [
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
]