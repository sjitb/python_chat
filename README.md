# python_chat
Building a Chat Client with Python and using Websockets and gRPC

### build virtual environment
poetry config virtualenvs.in-project true

### shell for poetry 2.0
poetry self add poetry-plugin-shell

### Generate gRPC code:
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/chat.proto

### Run servers (in separate terminals)
python grpc_server.py
python websocket_server.py

### Run clients (in separate terminals)
python grpc_client.py
python websocket_client.py
