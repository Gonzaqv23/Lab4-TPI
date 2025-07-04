from models.paquetes import Paquetes as PaquetesModel
from models.destinos import Destinos as DestinosModel
from schemas.paquetes import Paquetes
from fastapi import HTTPException
from typing import List

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
    
    def get_paquetes_por_destino(self, destino_id: int) -> List[PaquetesModel]:
        return self.db.query(PaquetesModel).filter(PaquetesModel.destino_id == destino_id).all()


    def create_paquete(self, Paquete: Paquetes):
        destino = self.db.query(DestinosModel).filter(DestinosModel.id == Paquete.destino_id).first()
        if not destino:
            raise HTTPException(status_code=404, detail="Destino no encontrado")
        new_paquete = PaquetesModel(**Paquete.model_dump(exclude={"id"}))
        self.db.add(new_paquete)
        self.db.commit()
        self.db.refresh(new_paquete)
        return
    
    def update_paquete(self, id: int, data: Paquetes):
        paquete = self.db.query(PaquetesModel).filter(PaquetesModel.id == id).first()
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

