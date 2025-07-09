from pydantic import BaseModel, Field
from datetime import date


class Paquetes(BaseModel):
    destino_id: int
    nombre: str = Field(min_length=5, max_length=50)
    precio: float = Field(ge=0)
    cupo: int = Field(ge=0)
    fecha_inicio: date
    fecha_fin: date

class PaqueteRespuesta(BaseModel):
    id: int
    destino_id: int
    nombre: str
    precio: float
    cupo: int
    fecha_inicio: date
    fecha_fin: date
    
    class Config:
        from_attributes = True

class PaqueteMini(BaseModel):
    nombre: str

    class Config:
        from_attributes = True