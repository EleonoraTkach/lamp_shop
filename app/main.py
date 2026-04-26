from fastapi import FastAPI, HTTPException
from schemas.product import Product, ProductCreate
import asyncpg
from db.db import DATABASE_URL
from db.db import init_db
from routers.catalog import router as catalog_router

app = FastAPI(
    title="Пример FastAPI",
    description="Простое in-memory API товаров",
    version="0.1.0",
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(catalog_router)

@app.get("/")
def read_root():
    return {"message": "Привет! Интерактивная документация: /docs и /redoc"}

@app.get("/health")
async def root():
    databases = await get_databases()
    return {"message": databases}

async def get_databases():
  conn = await asyncpg.connect(DATABASE_URL)
  try:
    result = await conn.fetch("SELECT datname FROM pg_database")
    return [record['datname'] for record in result]
  finally:
    await conn.close()
