from config.database import Base
from sqlalchemy import Column, Integer, String


class Usuarios(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(20))
    apellido = Column(String(20))
    correo = Column(String(100), unique=True)
    password = Column(String(1000))
    rol = Column(String(50))