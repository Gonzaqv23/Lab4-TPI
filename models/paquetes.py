from config.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date


class Paquetes(Base):

    __tablename__ = "paquetes"

    id  = Column(Integer, primary_key = True, autoincrement=True)
    destino_id = Column(Integer, ForeignKey('destinos.id'), nullable=False)
    nombre = Column(String(50))
    precio =  Column(Float(13,2))
    cupo = Column(Integer)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)