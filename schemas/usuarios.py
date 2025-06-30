from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class User(BaseModel):
    email: str
    password: str
class UsuarioBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=20)
    apellido: str = Field(min_length=2, max_length=20)
    correo: EmailStr
    rol: str

    class Config:
        from_attributes = True

class Usuarios(UsuarioBase):
    password: str = Field(min_length=8)

class UsuarioPublico(BaseModel):
    id: int
    nombre: str
    apellido: str
    correo: EmailStr
    rol: str

    class Config:
        from_attributes = True
