from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import json
from fastapi.encoders import jsonable_encoder
from database import get_db
from modules.message.message_scheme import Message as MessageScheme
from modules.user.user_service import set_online
from modules.user.user_scheme import User as UserScheme
import models

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
        self.online_users: dict[int, models.User] = {}

    def get_active_connections(self):
        user_list = list(map(lambda n: jsonable_encoder(UserScheme.model_validate(n)), self.online_users.values()))
        return { "users": user_list, "type": "users"}

    async def connect(self, websocket: WebSocket, client_id: int, db: Session):
        print(f"Client {client_id} connected")
        user = set_online(db, client_id)
        if user:
            self.online_users[client_id] = user
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(self.get_active_connections())
        await self.broadcast(self.get_active_connections())

    async def disconnect(self,  client_id: int, db: Session):
        print(f"Client {client_id} disconnected")
        user = set_online(db, client_id, False)
        if user:
            del self.online_users[client_id]
        del self.active_connections[client_id]
        print(self.get_active_connections())
        await self.broadcast(self.get_active_connections())

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def send_message_clinet(self, chat_id: int, message: models.Message, db: Session):
        chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
        print(self.active_connections.keys())
        data = {"type": "message", "data": jsonable_encoder(MessageScheme.model_validate(message))}
        if chat:
            if chat.user2ID in self.active_connections:
                await self.active_connections[chat.user2ID].send_json(data)
            if chat.user1ID in self.active_connections:
                await self.active_connections[chat.user1ID].send_json(data)


    async def broadcast(self, message: dict, client_id: str | None = None):
        for connection in self.active_connections:
            if client_id is None or not connection == client_id:
                await self.active_connections[connection].send_json(message)

ws_router = APIRouter(
    prefix="/ws",
    tags=["Websocket"]
)

manager = ConnectionManager()

@ws_router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await manager.connect(websocket, user_id, db)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(user_id, db)
