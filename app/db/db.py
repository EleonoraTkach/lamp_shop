import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from models import Product, Category


DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "super_secret_password")
DB_HOST = os.getenv("DB_HOST", "postgres_shop_db")
DB_NAME = os.getenv("DB_NAME", "shop")

DATABASE_URL = os.getenv("DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
