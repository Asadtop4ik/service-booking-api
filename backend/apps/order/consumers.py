import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer


class WorkerConsumer(AsyncWebsocketConsumer):
    group_name = "workers"

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notify(self, event):
        await self.send(text_data=json.dumps(event["payload"]))


class ClientConsumer(AsyncWebsocketConsumer):
    client_group = None

    async def connect(self):
        user = self.scope.get("user")
        client_id = None
        if user and user.is_authenticated and getattr(user, "role", None) == "client":
            client_id = user.id
        else:
            qs = parse_qs(self.scope.get("query_string", b"").decode())
            if "client_id" in qs:
                client_id = qs["client_id"][0]

        if not client_id:
            await self.close()
            return

        self.client_group = f"client_{client_id}"
        await self.channel_layer.group_add(self.client_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.client_group:
            await self.channel_layer.group_discard(self.client_group, self.channel_name)

    async def notify(self, event):
        await self.send(text_data=json.dumps(event["payload"]))
