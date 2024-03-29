from fastapi import FastAPI
from modules.chat.chat_controller import chat_router
from modules.user.user_controller import user_router
import uvicorn

import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(chat_router)
app.include_router(user_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
