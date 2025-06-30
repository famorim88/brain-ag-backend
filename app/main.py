from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import producer
from app.api import dashboard


app = FastAPI(
    title="Brain Agriculture API",
    description="API para gerenciar produtores rurais.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(producer.router)
app.include_router(dashboard.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API Brain Agriculture!"}