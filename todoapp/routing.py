from channels.routing import ProtocolTypeRouter, URLRouter

import apps.todos.routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        apps.todos.routing.websocket_urlpatterns
    )
})
