# chatapp/asgi.py
import os
import django
from django.core.asgi import get_asgi_application

# Définir le module de paramètres Django EN PREMIER
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp.settings")  # Remplacez "chatapp" par le nom réel de votre projet
django.setup()  # Initialiser Django explicitement

# Importer les dépendances après l'initialisation
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns  # Assurez-vous que ce chemin est correct

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})