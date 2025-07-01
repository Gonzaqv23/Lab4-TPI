from pydantic import BaseModel, Field
from typing import Optional, List


class Destinos(BaseModel):
    nombre: str = Field(min_length=5, max_length=50)
    descripcion: str = Field(max_length=100)
    pais: str = Field(max_length=100)

class DestinosOut(BaseModel):
    id: int
    nombre: str
    descripcion: str
    pais: str

    class Config:
        from_attributes = True