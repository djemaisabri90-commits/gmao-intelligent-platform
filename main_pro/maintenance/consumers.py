import json
from channels.generic.websocket import AsyncWebsocketConsumer

class InterventionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        await self.accept()
        if user.is_authenticated:
            await self.channel_layer.group_add(
                f"technicien_{user.id}", self.channel_name
            )
            await self.send(text_data=json.dumps({"message": "Connecté au groupe"}))

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
            await self.channel_layer.group_discard(
                f"technicien_{user.id}", self.channel_name
            )

    async def intervention_notification(self, event):
        await self.send(text_data=json.dumps(event["data"]))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            # Chaque technicien rejoint un groupe basé sur son ID
            await self.channel_layer.group_add(f"user_{user.id}", self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
            await self.channel_layer.group_discard(f"user_{user.id}", self.channel_name)

    async def receive(self, text_data):
        # Ici on peut gérer des messages entrants si besoin
        pass

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["message"]))

