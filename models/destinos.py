from config.database import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship


class Destinos(Base):

    __tablename__ = "destinos"

    id = Column(Integer, primary_key = True, autoincrement=True)
    nombre = Column(String(20))
    descripcion = Column(String(150))
    pais = Column(String(50))