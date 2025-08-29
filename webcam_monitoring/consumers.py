import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


class WebcamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'webcam_{self.session_id}'
        
        # Check if user is authenticated
        if self.scope["user"] == AnonymousUser():
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        frame_data = text_data_json.get('frame_data')
        analysis_type = text_data_json.get('analysis_type', 'attention')
        
        # Process frame data here (simplified)
        # In production, this would involve computer vision processing
        
        # Send analysis results back
        await self.send(text_data=json.dumps({
            'type': 'analysis_result',
            'analysis_type': analysis_type,
            'results': {
                'attention_score': 85,
                'emotion': 'focused',
                'timestamp': '2024-01-01T12:00:00Z'
            }
        }))
    
    async def analysis_update(self, event):
        # Send analysis update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'analysis_update',
            'data': event['data']
        }))