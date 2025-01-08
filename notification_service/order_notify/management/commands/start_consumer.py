from django.core.management.base import BaseCommand
from order_notify . consumer import start_consumer

class Command(BaseCommand):
    help = 'Start RabbitMQ consumer for notifications'

    def handle(self, *args, **kwargs):
        start_consumer()
