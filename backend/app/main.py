from fastapi import FastAPI
from pydantic import BaseModel
import databases
import sqlalchemy
from datetime import datetime

DATABASE_URL = "sqlite:///./chat.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

chat_history = sqlalchemy.Table(
    "chat_history",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("farmer_id", sqlalchemy.Integer),
    sqlalchemy.Column("message", sqlalchemy.Text),
    sqlalchemy.Column("sender", sqlalchemy.String),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime, default=datetime.utcnow)
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

class ChatMessage(BaseModel):
    farmer_id: int
    message: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/api/chat")
async def handle_chat(chat: ChatMessage):
    user_input = chat.message.lower()

    if 'fertilizer' in user_input:
        reply = "Apply 50 kg of nitrogen fertilizer per hectare."
    elif 'irrigation' in user_input:
        reply = "Water your fields early in the morning to reduce evaporation."
    elif 'pest' in user_input:
        reply = "Monitor for aphids and apply neem oil spray if needed."
    else:
        reply = "Please ask about irrigation, fertilizer, or pest control."

    query_insert_user = chat_history.insert().values(
        farmer_id=chat.farmer_id,
        message=chat.message,
        sender='Farmer',
        timestamp=datetime.utcnow()
    )
    await database.execute(query_insert_user)

    query_insert_system = chat_history.insert().values(
        farmer_id=chat.farmer_id,
        message=reply,
        sender='AgriSenseAI',
        timestamp=datetime.utcnow()
    )
    await database.execute(query_insert_system)

    return {"reply": reply}