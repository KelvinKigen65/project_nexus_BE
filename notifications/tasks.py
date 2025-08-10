from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

@shared_task
def send_order_confirmation_email(order_id):
    from orders.models import Order
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    
    order = Order.objects.get(pk=order_id)
    subject = f"Order Confirmation #{order.id}"
    html_message = render_to_string('emails/order_confirmation.html', {'order': order})
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        html_message=html_message
    )