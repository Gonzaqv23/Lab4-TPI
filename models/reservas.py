from config.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Date


class Reservas(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    paquete_id = Column(Integer, ForeignKey('paquete.id'), nullable=False)
    fecha_reserva = Column(Date)
    cant_personas = Column(Integer)