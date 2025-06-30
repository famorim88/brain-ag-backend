# backend/app/main.py
from fastapi import FastAPI
from api import producer # Importe seus routers aqui
# from backend.app.database.base import Base # Opcional: pode ser usado para criar tabelas
# from backend.app.database.session import engine # Opcional: para criar tabelas

app = FastAPI(
    title="Brain Agriculture API",
    description="API para gerenciar produtores rurais.",
    version="1.0.0",
)

# Inclua os routers da API
app.include_router(producer.router)
# Se você tiver mais routers (ex: dashboard), inclua-os aqui também:
# from backend.app.api import dashboard
# app.include_router(dashboard.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API Brain Agriculture!"}