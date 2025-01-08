import pika
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
import os


USER_SERVICE_URL= os.getenv('USER_SERVICE_URL')
PRODUCT_SERVICE_URL= os.getenv('PRODUCT_SERVICE_URL')


class OrderView(APIView):
    def send_notification(self, message):
        # connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='order_notifications')
        
        message = json.dumps(message)
        channel.basic_publish(
            exchange='',
            routing_key='order_notifications',
            body= message
            # properties=pika.BasicProperties(
            #     delivery_mode=pika.DeliveryMode.Persistent
            # )
        )
        connection.close()


    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        price = request.data.get('price')
        print(user_id, product_id, quantity, price)
        try:
            auth_token = request.headers.get('Authorization')
        except Exception as e:
            print(e)
            return Response({"error": "Authorization token needed"}, status=500)


        # Validate user
        try:
            headers = {
                'Authorization': auth_token  # Pass the token in the headers to the user service
            }
            # user_response = requests.get(f"http://localhost:8001/api/users/{user_id}") # for local running
            # user_response = requests.get(f"http://host.docker.internal:8001/api/users/{user_id}/") # if you're running docker container in bridge network
            # user_response = requests.get(f"http://user-service:8001/api/users/{user_id}/", headers=headers) # for kuberenetes running.
            user_response = requests.get(f"{USER_SERVICE_URL}/api/users/{user_id}/", headers=headers)
            print(user_response)
            print(user_response.status_code)
            if user_response.status_code != 200:
                return Response({"error": "Invalid user ID"}, status=400)
            user_data = user_response.json()

        except requests.exceptions.RequestException as e:
            print('error++++++++++++++++++++++++++++++++++++++++++++++++\n',e)
            return Response({"error": "Error connecting to User Service"}, status=500)

        # Validate product availability
        try:
            # product_response = requests.get(f"http://localhost:8002/api/products/{product_id}/")
            # user_response = requests.get(f"http://host.docker.internal:8002/api/products/{product_id}/") # if you're running docker container in bridge network
            # product_response = requests.get(f"http://product-service:8002/api/products/{product_id}/")
            product_response = requests.get(f"{PRODUCT_SERVICE_URL}/api/products/{product_id}/")
            print(product_response)
            print(product_response.status_code)
            if product_response.status_code != 200:
                return Response({"error": "Invalid product ID"}, status=400)

            product_data = product_response.json()

            if product_data['stock'] < quantity:
                return Response({"error": "Insufficient stock"}, status=400)
            
            if product_data['price'] != price:
                return Response({"error": "Price mismatch"}, status=400)

        except requests.exceptions.RequestException as e:
            import traceback
            print(traceback.format_exc())  
            print(e)
            return Response({"error": "Error connecting to Product Service"}, status=500)
        
        message = {**user_data, **product_data}
        message['qty'] = quantity
        
        # self.send_notification(message=message) # for test
        # return Response(status=status.HTTP_201_CREATED)

        # Create the order
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # Deduct stock in Product Service
            try:
                # isn't the below method dangerous? if multiple party ordered at a time all will get same quantity as response then when updating the quantity using patch only the last updated stock - quantity will reflect.
                # may be we have to use gRPC or message broker.
                stock_update_response = requests.patch(
                    # f"http://localhost:8002/api/products/{product_id}/",
                    # f"http://host.docker.internal:8002/api/products/{product_id}/", # if you're running docker container in bridge network
                    # f"http://product-service:8002/api/products/{product_id}/",
                    f"{PRODUCT_SERVICE_URL}/api/products/{product_id}/",
                    json={"stock": product_data['stock'] - quantity}
                )
                if stock_update_response.status_code != 200:
                    return Response({"error": "Failed to update product stock"}, status=500)
                
            except requests.exceptions.RequestException as e:
                return Response({"error": "Error updating product stock"}, status=500)

            # Send a message to RabbitMQ for notifications
            self.send_notification(message)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrderView(APIView):
    def get(self, request, pk):
        orders = Order.objects.filter(user_id=pk)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    

class ProductOrderView(APIView):
    def get(self, request, pk):
        orders = Order.objects.filter(product_id=pk)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
