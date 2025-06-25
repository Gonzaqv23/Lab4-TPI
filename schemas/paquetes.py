from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class Paquetes(BaseModel):
    id: Optional[int] = None
    destino_id: int
    nombre: str = Field(min_length=5, max_length=50)
    precio: float
    cupo: int
    fecha_inicio: date
    fecha_fin: date

