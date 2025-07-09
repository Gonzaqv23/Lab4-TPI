from models.reservas import Reservas as ReservasModel
from models.usuarios import Usuarios as UsuariosModel
from models.paquetes import Paquetes as PaquetesModel
from schemas.reservas import Reservas
from fastapi import HTTPException
from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import joinedload

class ReservasService():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_reservas(self):
        result = self.db.query(ReservasModel)\
        .options(
            joinedload(ReservasModel.usuario),
            joinedload(ReservasModel.paquete)
        ).all()
        return result

    def get_reserva_id(self, id):
        result = self.db.query(ReservasModel).filter(ReservasModel.id == id).first()
        return result
    
    def get_reservas_activas_por_usuario(self, usuario_id: int):
        hoy = date.today()
    
        return (
            self.db.query(ReservasModel)
            .join(PaquetesModel, ReservasModel.paquete_id == PaquetesModel.id)
            .filter(
                ReservasModel.usuario_id == usuario_id,
                PaquetesModel.fecha_inicio <= hoy,
                PaquetesModel.fecha_fin >= hoy
            )
            .all()
        )
    
    def get_historial_de_viajes(self, usuario_id: int):
        hoy = date.today()
        
        return (
            self.db.query(ReservasModel)
            .join(PaquetesModel, ReservasModel.paquete_id == PaquetesModel.id)
            .filter(
                ReservasModel.usuario_id == usuario_id,
                PaquetesModel.fecha_fin < hoy
            )
            .all()
        )

    
    def create_reserva(self, Reserva: Reservas):
        usuario = self.db.query(UsuariosModel).filter(UsuariosModel.id == Reserva.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        paquete = self.db.query(PaquetesModel).filter(PaquetesModel.id == Reserva.paquete_id).first()
        if not paquete:
            raise HTTPException(status_code=404, detail="Paquete no encontrado")
        total_reservado = (self.db.query(func.coalesce(func.sum(ReservasModel.cantidad_personas), 0))
        .filter(ReservasModel.paquete_id == Reserva.paquete_id)
        .scalar())
        if total_reservado + Reserva.cantidad_personas > paquete.cupo:
            lugares_restantes = max(paquete.cupo - total_reservado, 0)
            raise HTTPException(status_code=400,
                                detail=f"No hay cupo suficiente. Solo quedan {lugares_restantes} lugares disponibles.")
        new_reserva = ReservasModel(**Reserva.model_dump(exclude={"id"}))
        self.db.add(new_reserva)
        self.db.commit()
        self.db.refresh(new_reserva)
        return
    
    def update_reserva(self, id: int, data: Reservas):
        reserva = self.db.query(ReservasModel).filter(ReservasModel.id == id).first()
        reserva.usuario_id = data.usuario_id
        reserva.paquete_id = data.paquete_id
        reserva.fecha_reserva = data.fecha_reserva
        reserva.cantidad_personas = data.cantidad_personas

        self.db.commit()
        return
    
    def delete_reserva(self, id: int):
       self.db.query(ReservasModel).filter(ReservasModel.id == id).delete()
       self.db.commit()
       return