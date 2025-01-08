from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^api/users/.*$', views.proxy_to_user_service, name='proxy-user'),
    re_path(r'^api/products/.*$', views.proxy_to_product_service, name='proxy-product'),
    re_path(r'^api/orders/.*$', views.proxy_to_order_service, name='proxy-order'),
]
