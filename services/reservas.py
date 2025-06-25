from models.reservas import Reservas as ReservasModel
from schemas.reservas import Reservas

class ReservasService():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_reservas(self):
        result = self.db.query(ReservasModel).all()
        return result

    def get_reserva_id(self, id):
        result = self.db.query(ReservasModel).filter(ReservasModel.id == id).first()
        return result
    
    def create_reserva(self, Reserva: Reservas):
        new_producto = ReservasModel(**Reserva.model_dump(exclude={'emailUsuario', 'nombreProducto'})  )
        self.db.add(new_producto)
        self.db.commit()
        return
    
    def update_reserva(self, id: int, data: Reservas):
        reserva = self.db.query(ReservasModel).filter(ReservasModel.id == id).first()
        reserva.usuario_id = data.usuario_id
        reserva.paquete_id = data.paquete_id
        reserva.fecha = data.fecha
        reserva.cant_pers = data.cant_personas

        self.db.commit()
        return
    
    def delete_reserva(self, id: int):
       self.db.query(ReservasModel).filter(ReservasModel.id == id).delete()
       self.db.commit()
       return

