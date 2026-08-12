# maintenance/routing.py
from django.urls import re_path
from .consumers import InterventionConsumer
from .consumers import NotificationConsumer
"""
websocket_urlpatterns = [
    re_path(r"ws/interventions/$", InterventionConsumer.as_asgi()),
    #re_path(r"ws/workorders/$", InterventionConsumer.as_asgi()),
    re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
]
"""

websocket_urlpatterns = [
    re_path(r"ws/interventions/$", InterventionConsumer.as_asgi()),
    re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
]