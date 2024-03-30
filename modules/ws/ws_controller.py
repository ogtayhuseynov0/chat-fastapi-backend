from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import json
from database import get_db
from modules.user.user_service import set_online

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    def get_active_connections(self):
        return { "users": list(self.active_connections.keys()), "type": "users"}

    async def connect(self, websocket: WebSocket, client_id: str, db: Session):
        print(f"Client {client_id} connected")
        set_online(db, client_id)
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(self.get_active_connections())
        await self.broadcast(self.get_active_connections())

    async def disconnect(self,  client_id: str, db: Session):
        print(f"Client {client_id} disconnected")
        set_online(db, client_id, False)
        del self.active_connections[client_id]
        print(self.get_active_connections())
        await self.broadcast(self.get_active_connections())

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict, client_id: str | None = None):
        for connection in self.active_connections:
            if client_id is None or not connection == client_id:
                await self.active_connections[connection].send_json(message)

ws_router = APIRouter(
    prefix="/ws",
    tags=["Websocket"]
)

manager = ConnectionManager()

@ws_router.websocket("/{user_name}")
async def websocket_endpoint(websocket: WebSocket, user_name: str, db: Session = Depends(get_db)):
    await manager.connect(websocket, user_name, db)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(user_name, db)
