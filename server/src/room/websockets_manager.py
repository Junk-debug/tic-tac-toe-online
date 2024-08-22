import json

from starlette.websockets import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, key: int, websocket: WebSocket):
        await websocket.accept()
        if key not in self.active_connections:
            self.active_connections[key] = []
        self.active_connections[key].append(websocket)

    async def disconnect(self, key: int, websocket: WebSocket):
        self.active_connections[key].remove(websocket)

    def destroy_the_connection(self, key: int):
        if key in self.active_connections:
            del self.active_connections[key]

    @staticmethod
    async def send_personal_message(message: dict, websocket: WebSocket):
        json_message = json.dumps(message)
        await websocket.send_text(json_message)

    async def broadcast(self, key: int, message: dict):
        if key in self.active_connections:
            json_message = json.dumps(message)
            for connection in self.active_connections[key]:
                await connection.send_text(json_message)

manager = ConnectionManager()
