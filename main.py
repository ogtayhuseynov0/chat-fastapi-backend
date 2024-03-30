from fastapi import FastAPI
from modules.chat.chat_controller import chat_router
from modules.message.message_controller import message_router
from modules.user.user_controller import user_router
from modules.ws.ws_controller import ws_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


import models
from database import engine

models.Base.metadata.create_all(bind=engine)
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(user_router)
app.include_router(ws_router)
app.include_router(message_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
