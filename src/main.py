from fastapi import FastAPI

from src.routes import whatsapp

app = FastAPI()
app.include_router(whatsapp)
