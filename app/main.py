from fastapi import FastAPI

from app.emails.router import router as email_router
import app.models # noqa: F401


app = FastAPI(title="Tempmail Service")

# Подключение роутера ящиков.
app.include_router(email_router)


@app.get("/health")
def health_check():
    return {"status": "alive"}
