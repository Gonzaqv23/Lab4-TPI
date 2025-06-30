from pydantic import BaseModel
from typing import List, Optional

class UsuarioResumen(BaseModel):
    id: int
    nombre: str
    apellido: str
    total_reservas: int

class PaqueteResumen(BaseModel):
    id: int
    nombre: str
    personas_reservadas: int

class DashboardStats(BaseModel):
    total_destinos: int
    reservas_activas: int
    usuarios_destacados: List[UsuarioResumen]
    paquete_mas_reservado: Optional[PaqueteResumen]
