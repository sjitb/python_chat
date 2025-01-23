from asyncio import Queue
import grpc
from concurrent import futures
import time
from datetime import datetime
from proto.chat_pb2 import ChatMessage, ChatResponse
from proto.chat_pb2_grpc import ChatServiceServicer, add_ChatServiceServicer_to_server

class ChatServicer(ChatServiceServicer):
    def __init__(self):
        self.messages = []
        self.subscribers = []
    
    def SendMessage(self, request, context):
        message = {
            'user_id': request.user_id,
            'content': request.content,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.messages.append(message)
        
        # Notify all subscribers
        for subscriber in self.subscribers:
            subscriber.put(message)
            
        return ChatResponse(success=True, message="Message sent successfully")
    
    def StreamMessages(self, request, context):
        # Create queue for this subscriber
        queue = Queue()
        self.subscribers.append(queue)
        
        try:
            while True:
                message = queue.get()
                yield ChatMessage(
                    user_id=message['user_id'],
                    content=message['content'],
                    timestamp=message['timestamp']
                )
        except Exception as e:
            self.subscribers.remove(queue)

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ChatServiceServicer_to_server(ChatServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server started on port 50051")
    server.wait_for_termination()
