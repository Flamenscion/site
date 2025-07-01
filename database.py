import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Загрузить .env
load_dotenv()

# Получить URL из .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Создать асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Dependency для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
