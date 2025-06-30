from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from models.destinos import Destinos as DestinosModel
from models.paquetes import Paquetes as PaquetesModel
from models.reservas import Reservas as ReservasModel
from models.usuarios import Usuarios as UsuariosModel


class DashboardService:
    def __init__(self, db):
        self.db = db

    def contar_destinos(self) -> int:
        return self.db.query(func.count(DestinosModel.id)).scalar()

    def contar_reservas_activas(self) -> int:
        hoy = date.today()
        return (
            self.db.query(ReservasModel)
            .join(PaquetesModel)
            .filter(
                PaquetesModel.fecha_inicio <= hoy,
                PaquetesModel.fecha_fin >= hoy
            )
            .count()
        )

    def top_usuarios_por_reservas(self, limite: int = 5):
        return (
            self.db.query(
                UsuariosModel.id,
                UsuariosModel.nombre,
                UsuariosModel.apellido,
                func.count(ReservasModel.id).label("total_reservas")
            )
            .join(ReservasModel)
            .group_by(UsuariosModel.id)
            .order_by(func.count(ReservasModel.id).desc())
            .limit(limite)
            .all()
        )

    def paquete_mas_reservado(self):
        return (
            self.db.query(
                PaquetesModel.id,
                PaquetesModel.nombre,
                func.sum(ReservasModel.cantidad_personas).label("personas_reservadas")
            )
            .join(ReservasModel)
            .group_by(PaquetesModel.id)
            .order_by(func.sum(ReservasModel.cantidad_personas).desc())
            .first()
        )
