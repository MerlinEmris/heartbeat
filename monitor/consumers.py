import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ScanConsumer(WebsocketConsumer):

    def __int__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None

    def connect(self):
        self.accept()
        self.user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)(
            self.user.username,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.user.username,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        data = text_data_json['data']

        if not self.user.is_authenticated:
            return

        async_to_sync(self.channel_layer.group_send)(
            self.user.username,
            {
                'type': 'state.info',
                'data': data,
            }
        )




    def scan_data(self,event: dict):
        self.send(text_data=json.dumps(event))

    def state_info(self, event: dict):
        self.send(text_data=json.dumps(event))