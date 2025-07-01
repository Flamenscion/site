from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str
    phone: str = Field(..., pattern=r'^(\+7|8)\d{10}$')  # строго KZ номер 📞

class UserRead(BaseModel):
    id: int
    name: str
    phone: str

    class Config:
        orm_mode = True
