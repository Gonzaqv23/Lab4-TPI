from config.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.usuarios import Usuarios
from models.paquetes import Paquetes


class Reservas(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    paquete_id = Column(Integer, ForeignKey('paquetes.id'), nullable=False)
    fecha_reserva = Column(Date)
    cantidad_personas = Column(Integer)

    usuario = relationship(Usuarios)
    paquete = relationship(Paquetes)