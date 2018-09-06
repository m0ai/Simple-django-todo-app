from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class TodoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'todos_app',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'todos_app',
            self.channel_name
        )

    async def notify_delete(self, event):
        event['type']  = 'delete'
        await self.send_json(event)

    # notify working at create or update a someting to Todo model
    async def update_or_create(self, event):
        await self.send_json(event)
