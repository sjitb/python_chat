
# websocket_client.py
import asyncio
import websockets
import json

async def connect_websocket():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Handle receiving messages
        async def receive_messages():
            while True:
                message = await websocket.recv()
                print(f"Received message: {message}")
        
        # Handle sending messages
        async def send_messages():
            while True:
                message = input("Enter message: ")
                await websocket.send(json.dumps({
                    'user_id': 'user1',
                    'content': message
                }))
        
        await asyncio.gather(receive_messages(), send_messages())

        