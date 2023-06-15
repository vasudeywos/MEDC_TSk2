from django.shortcuts import render
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from .models import Message
from users.models import User
from channels.db import database_sync_to_async


def room(request, staff_username, patient_username):
    room_name = f"{staff_username}_{patient_username}"
    staff = User.objects.get(username=staff_username)
    patient = User.objects.get(username=patient_username)
    messages = Message.objects.filter(room_name=room_name)
    return render(request, "chat/chat.html", {"room_name": room_name, "messages": messages, "staff": staff, "patient": patient})


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        recipient_username = self.scope["user"].username
        await self.mark_messages_as_seen(recipient_username)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json["username"]
        message = text_data_json["message"]

        member = await sync_to_async(User.objects.get)(username=username)
        await sync_to_async(Message.objects.create)(
            room_name=self.room_name, author=member, content=message
        )
        await self.channel_layer.group_send(self.room_group_name, {
            "type": "chat_message",
            "message": message,
            "username": username
        })

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))

        recipient_username = self.scope["user"].username
        sender_username = username

        if sender_username != recipient_username:
            await self.mark_messages_as_seen(sender_username)

    @database_sync_to_async
    def mark_messages_as_seen(self, username):
        messages = Message.objects.filter(room_name=self.room_name)
        for message in messages:
            if message.author.username != username:
                message.is_seen = True
                message.save()

