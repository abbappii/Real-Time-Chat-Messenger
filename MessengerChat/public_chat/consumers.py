from curses import noraw
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils import timezone
from datetime import datetime

from public_chat.models import PublicChatRoom, PublicRoomMessage

User = get_user_model()

MSG_TYPE_MESSAGE = 0


# Example taken from:
# https://github.com/andrewgodwin/channels-examples/blob/master/multichat/chat/consumers.py


class PublicChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        print("PublicChatConsumer: connect: " + str(self.scope["user"]))
        # let everyone connect. But limit read/write to authenticated users
        await self.accept()
        self.room_id = None

        # Add them to the group so they get room messages
        # await self.channel_layer.group_add(
        #     "public_chatroom_1",
        #     self.channel_name,
        # )


    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # leave the room
        print("PublicChatConsumer: disconnect")
        try:
            if self.room_id != None:
                self.leave_room(self.room_id)
        except Exception:
            pass


    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        print("PublicChatConsumer: receive_json: " + str(command))
        # print("PublicChatConsumer: receive_json: message: " +
        #       str(content["message"]))

        try:
            if command == "send":
                if len(content['message'].lstrip()) == 0:
                    raise ClientError(422,"you cant't send an emppty message.")
                # await self.send_message(content['room'])
                await self.send_room(content['room_id'], content['message'])
            elif command == "join":
                await self.join_room(content['room'])
            elif command == 'leave':
                await self.leave_room(content['room'])

        except ClientError as e:
            # errorData = {}
            # errorData['error'] = e.code
            # if e.message:
            #     errorData['message'] = e.message
            # await self.send_json(errorData)
            await self.handle_client_error(e)

        

    async def send_room(self,room_id,message):
        """
        Called by receive_json when someone sends a message to a room.
        """
        print("publicChatConsumer: send_room")
        if self.room_id != None:
            if str(room_id) != str(self.room_id):
                raise ClientError("Room Access Denied","room access denied")
            if not is_authenticated(self.scope["user"]):
                raise ClientError("auth_error","you must be authenticated")
        else:
            raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")

        # get the room and send to the group about it 
        room = await get_room_or_error(room_id)

        await create_public_room_chat_message(self.scope["user"],room, message)

		# Check they are in this room
        await self.channel_layer.group_send(
            # "public_chatroom_1",
            room.group_name,
            {
                "type": "chat.message",
                "profile_image": self.scope["user"].profile_image.url,
                "username": self.scope["user"].username,
                        "user_id": self.scope["user"].id,
                        "message": message,
            }
        )

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        print("PublicChatConsumer: chat_message from user #" +
              str(event["user_id"]))
        
        now = timezone.now()
        print("now time is:",now)
        timestamp = calculate_timestamp(now)

        print("timestamp time:", timestamp)

        await self.send_json(
            {
                "msg_type": MSG_TYPE_MESSAGE,
                "profile_image": event["profile_image"],
                "username": event["username"],
                "user_id": event["user_id"],
                "message": event["message"],
                "timestamp": timestamp,
            },
        )

    async def join_room(self, room_id):
        """
		Called by receive_json when someone sent a join command.
		"""
        print("PublicChatConsumer: join_room")

        is_auth_user = is_authenticated(self.scope['user'])

        try:
            room = await get_room_or_error(room_id)
        except ClientError as e:
            await self.handle_client_error(e)

        # Add user to "users" list for room
        if is_auth_user:
            await connect_user(room,self.scope["user"])

        # Store that we are in 
        self.room_id = room.id
        
        # add them to group so that can send msg 
        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )
		# Instruct their client to finish opening the room
        await self.send_json({
            "join":str(room.id)
        })
    
    async def leave_room(self, room_id):
        """
		Called by receive_json when someone sent a leave command.
		"""
        print("PublicChatConsumer: leave_room")

        is_auth = is_authenticated(self.scope["user"])
        room = await get_room_or_error(room_id)

		# Remove user from "users" list
        if is_auth:
            disconnected_user(room,self.scope['user'])

        # remove that we are in the room 
        self.room_id = None
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )

    async def handle_client_error(self,e):
        errorData = {}
        errorData['error'] = e.code

        if e.message:
            errorData['message'] = e.message
            await self.send_json(errorData)
        return 

class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code, message):
        super().__init__(code)
        self.code = code
        if message:
        	self.message = message


# authentication func 
def is_authenticated(user):
    if user.is_authenticated:
        return True
    return False

# db sync to async connect user 
@database_sync_to_async
def connect_user(room,user):
    return room.connect_user(user)

@database_sync_to_async
def disconnected_user(room,user):
    return room.disconnected_user(user)

@database_sync_to_async
def get_room_or_error(room_id):
    # Try to fetch a room  for user 
    try:
        room = PublicChatRoom.objects.get(pk=room_id)
    except PublicChatRoom.DoesNotExist:
        raise ClientError("Room_Invalid","Invalid room.")
    return room


@database_sync_to_async
def create_public_room_chat_message(user,room,message):
    return PublicRoomMessage.objects.create(user=user, room = room , content = message)



def calculate_timestamp(timestamp):
    ts = ""
    if (naturalday(timestamp) == 'today') or (naturalday(timestamp) == "yesterday"):
        str_time = datetime.strftime(timestamp, "%I:%M %p")
        print("first without strip:",str_time)
        str_time  = str_time.strip("0")
        print("after strip time",str_time)
        ts = f"{naturalday(timestamp)} at {str_time}" 
        print("ts : ", ts)

    else:
        str_time = datetime.strftime(timestamp,"%m/%d/%Y")
        print("else case str_time: ", str_time)
        ts = f"{str_time}"
        print("else case ts: ", ts)
