from fastapi import FastAPI

from app.emails.router import router as email_router
from app.messages.router import router as messages_router
from app.messages.router import webhook_router 
import app.models # noqa: F401


app = FastAPI(title="Tempmail Service")

# Подключение роутера ящиков.
app.include_router(email_router)
app.include_router(messages_router)
app.include_router(webhook_router)

@app.get("/health")
def health_check():
    return {"status": "alive"}
