from fastapi import FastAPI, HTTPException
import asyncpg
from db import DATABASE_URL
from db import init_db
from routers import order_router,order_item_router

app = FastAPI(
    title="Пример FastAPI",
    description="Простое in-memory API товаров",
    version="0.1.0",
)

@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(order_router)
app.include_router(order_item_router)

@app.get("/")
def read_root():
    return {"message": "Привет! Интерактивная документация: /docs и /redoc"}

'''
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
'''
