from models.destinos import Destinos as DestinosModel
from schemas.destinos import Destinos

class DestinosService():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_destinos(self):
        result = self.db.query(DestinosModel).all()
        return result

    def get_destino_id(self, id):
        result = self.db.query(DestinosModel).filter(DestinosModel.id == id).first()
        return result
    
    def get_destinos_nombre(self, nombre):
        result = self.db.query(DestinosModel).filter(DestinosModel.nombre == nombre).first()
        return result
    
    def get_destinos_pais(self, pais):
        result = self.db.query(DestinosModel).filter(DestinosModel.pais == pais).first()
        return result

    def create_destino(self, Destino: Destinos):
        new_producto = DestinosModel(**Destino.model_dump(exclude={'destino'}) )
        self.db.add(new_producto)
        self.db.commit()
        return
    
    def update_destino(self, id: int, data: Destinos):
        destino = self.db.query(DestinosModel).filter(DestinosModel.id == id).first()
        destino.nombre = data.nombre
        destino.descripcion = data.descripcion
        destino.pais = data.pais
        self.db.commit()
      
        return
    
    def delete_destino(self, id: int):
       self.db.query(DestinosModel).filter(DestinosModel.id == id).delete()
       self.db.commit()
       return


