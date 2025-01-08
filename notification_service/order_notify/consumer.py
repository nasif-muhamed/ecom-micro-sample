import pika
import json

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def send_review_email_task(email, subject, body):
    email = EmailMessage(
        subject, body,
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    return email.send(fail_silently=False)

def callback(ch, method, properties, body):
    order_data = json.loads(body)
    print(f"[x] Received: {order_data}")
    product_name = order_data['name']
    recipient_email = order_data['email']
    email_subject = f"Order for {product_name} is placed successfully"
    ttl = order_data['qty'] * float(order_data['price'])
    
    context = {
        'username': order_data['username'],
        'product': product_name,
        'description': order_data['description'],
        'price': order_data['price'],
        'qty': order_data['qty'],
        'ttl': ttl,
    }
    
    email_body = render_to_string('email_message.txt', context)
    send_review_email_task(recipient_email, email_subject, email_body)

def start_consumer():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='order_notifications')

    print("[*] Waiting for messages. To exit press CTRL+C")
    channel.basic_consume(
        queue='order_notifications', on_message_callback=callback, auto_ack=True
    )

    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
