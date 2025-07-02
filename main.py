from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models, database
from models import User
from database import get_db
from schemas import UserCreate, UserRead
from fastapi.middleware.cors import CORSMiddleware


import os
from dotenv import load_dotenv
load_dotenv()
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

# 📩 Импорт отправки письма
from utils.email_sender import send_user_email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def on_startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/")
async def read_root():
    return {"message": "FastAPI + MySQL подключено успешно!"}

@app.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.phone == user.phone))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким номером уже существует 📱")

    new_user = User(name=user.name, phone=user.phone)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # ✅ Отправка письма админу
    send_user_email(name=user.name, phone=user.phone, to_email=ADMIN_EMAIL)

    return new_user

@app.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден 😿")
    return user
