import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
import practiceblog.routing

ASGI_APPLICATION = 'mysite.asgi.application'

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  # Just HTTP for now. (We can add other protocols later.)
  "websocket": AuthMiddlewareStack(
        URLRouter([
            practiceblog.routing.websocket_urlpatterns[0],
            practiceblog.routing.websocket_urlpatterns[1],
            practiceblog.routing.websocket_urlpatterns[2],
        ])
    ),
})