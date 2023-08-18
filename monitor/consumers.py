import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class ScanConsumer(AsyncWebsocketConsumer):

    def __int__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None

    async def connect(self):
        await self.accept()
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            self.user.username,
            self.channel_name,
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user.username,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        data = text_data_json['data']

        if not self.user.is_authenticated:
            return

        await self.channel_layer.group_send(
            self.user.username,
            {
                'type': 'state.info',
                'data': data,
            }
        )




    async def scan_data(self,event: dict):
        await self.send(text_data=json.dumps(event))

    async def state_info(self, event: dict):
        await self.send(text_data=json.dumps(event))