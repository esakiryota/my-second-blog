import os

import django
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

ASGI_APPLICATION = 'mysite.asgi.application'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  # Just HTTP for now. (We can add other protocols later.)
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})