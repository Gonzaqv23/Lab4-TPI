from pydantic import BaseModel, Field
from datetime import date
from schemas.usuarios import UsuarioMini
from schemas.paquetes import PaqueteMini


class Reservas(BaseModel):
    usuario_id: int
    paquete_id: int
    fecha_reserva: date
    cantidad_personas: int = Field(gt=0)

class ReservaRespuesta(BaseModel):
    id: int
    fecha_reserva: date
    cantidad_personas: int
    usuario: UsuarioMini
    paquete: PaqueteMini

    class Config:
        from_attributes = True