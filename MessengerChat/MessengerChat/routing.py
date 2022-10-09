from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path
from django.core.asgi import get_asgi_application
from channels.http import AsgiHandler

from public_chat.consumers import PublicChatConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
	'websocket': AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter([
					path('public_chat/<room_id>/', PublicChatConsumer.as_asgi()),
			])
		)
	),
})