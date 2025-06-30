from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class Paquetes(BaseModel):
    destino_id: int
    nombre: str = Field(min_length=5, max_length=50)
    precio: float = Field(ge=0)
    cupo: int = Field(ge=0)
    fecha_inicio: date
    fecha_fin: date