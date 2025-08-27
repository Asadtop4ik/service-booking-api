from django.urls import re_path

from .consumers import ClientConsumer, WorkerConsumer

websocket_urlpatterns = [
    re_path(r"ws/orders/workers/$", WorkerConsumer.as_asgi()),
    re_path(r"ws/orders/client/$", ClientConsumer.as_asgi()),
]
