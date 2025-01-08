from django.db import models

class Order(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
