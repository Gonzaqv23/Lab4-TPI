from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class Reservas(BaseModel):
    usuario_id: int
    paquete_id: int
    fecha_reserva: date
    cantidad_personas: int = Field(gt=0)

class ReservaCreate(BaseModel):
    paquete_id: int
    fecha_reserva: date
    cantidad_personas: int = Field(gt=0)