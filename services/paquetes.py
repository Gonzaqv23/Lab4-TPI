from models.paquetes import Paquetes as PaquetesModel
from schemas.paquetes import Paquetes

class PaquetesService():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_paquetes(self):
        result = self.db.query(PaquetesModel).all()
        return result

    def get_paquete_id(self, id):
        result = self.db.query(PaquetesModel).filter(PaquetesModel.id == id).first()
        return result
    
    def get_paquete_destino(self, destino_id):
        result = self.db.query(PaquetesModel).filter(PaquetesModel.destino_id == destino_id).first()
        return result

    def create_paquete(self, Paquete: Paquetes):
        new_categoria = PaquetesModel(**Paquete.model_dump())
        self.db.add(new_categoria)
        self.db.commit()
        return
    
    def update_paquete(self, id: int, data: Paquetes):
        paquete = self.db.query(PaquetesModel).filter(PaquetesModel.id == id).first()
        paquete.destino_id = data.destino_id
        paquete.nombre = data.nombre
        paquete.precio = data.precio
        paquete.cupo = data.cupo
        paquete.fecha_inicio = data.fecha_inicio
        paquete.fecha_fin = data.fecha_fin
        self.db.commit()
        return
    
    def delete_paquete(self, id: int):
       self.db.query(PaquetesModel).filter(PaquetesModel.id == id).delete()
       self.db.commit()
       return

