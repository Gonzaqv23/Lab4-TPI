from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class Reservas(BaseModel):
    id: Optional[int] = None
    usuario_id: int
    paquete_id: int
    fecha: date
    cant_personas: int

