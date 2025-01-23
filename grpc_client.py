import grpc
from proto.chat_pb2 import ChatMessage, Empty
from proto.chat_pb2_grpc import ChatServiceStub
from concurrent.futures import ThreadPoolExecutor
import threading

class ChatClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = ChatServiceStub(self.channel)
    
    def send_message(self, user_id, content):
        message = ChatMessage(
            user_id=user_id,
            content=content
        )
        response = self.stub.SendMessage(message)
        return response
    
    def stream_messages(self):
        empty = Empty()
        try:
            for message in self.stub.StreamMessages(empty):
                print(f"Received: {message.user_id}: {message.content}")
        except grpc.RpcError as e:
            print(f"Stream ended: {e}")
