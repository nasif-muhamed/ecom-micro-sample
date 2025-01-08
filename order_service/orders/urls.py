from django.urls import path
from .views import OrderView, UserOrderView, ProductOrderView

urlpatterns = [
    path('orders/', OrderView.as_view(), name='orders'),
    path('orders/user/<int:pk>/', UserOrderView.as_view(), name='user-orders'),
    path('orders/product/<int:pk>/', ProductOrderView.as_view(), name='product-orders'),
    # path('orders/test/', TestPurose1.as_view(), name='test'),

]
