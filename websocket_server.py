import asyncio
import websockets
import json

class ChatWebSocket:
    def __init__(self):
        self.clients = set()
        self.messages = []
    
    async def register(self, websocket):
        self.clients.add(websocket)
    
    async def unregister(self, websocket):
        self.clients.remove(websocket)
    
    async def broadcast(self, message):
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients]
            )
    
    async def handler(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                chat_message = {
                    'user_id': data['user_id'],
                    'content': data['content'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.messages.append(chat_message)
                await self.broadcast(chat_message)
        finally:
            await self.unregister(websocket)

async def serve_websocket():
    chat = ChatWebSocket()
    async with websockets.serve(chat.handler, 'localhost', 8765):
        print("WebSocket Server started on port 8765")
        await asyncio.Future()  # run forever
