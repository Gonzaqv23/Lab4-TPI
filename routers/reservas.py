from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import get_database_session
from models.reservas import Reservas as ReservasModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.reservas import ReservasService
from schemas.reservas import Reservas

reservas_router = APIRouter()

@reservas_router.get('/reservas', tags=['Reservas'], response_model=List[Reservas], status_code=200, dependencies=[Depends(JWTBearer())])
def get_reservas(db = Depends(get_database_session)) -> List[Reservas]:
    #db = Session()
    result = ReservasService(db).get_reservas()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@reservas_router.get('/reservas/{id}', tags=['Reservas'], response_model=Reservas)
def get_reserva(id: int = Path(ge=1, le=2000), db = Depends(get_database_session)) -> Reservas:
    #db = Session()
    result = ReservasService(db).get_reserva_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@reservas_router.post('/reservas', tags=['Reservas'], response_model=dict, status_code=201)
def create_reservas(reserva: Reservas, db = Depends(get_database_session)) -> dict:
    #db = Session()
    ReservasService(db).create_reserva(reserva)
    return JSONResponse(status_code=201, content={"message": "Se registro la reserva"})


@reservas_router.put('/reservas/{id}', tags=['Reservas'], response_model=dict, status_code=200)
def update_reservas(id: int, reservas: Reservas, db = Depends(get_database_session))-> dict:
    #db = Session()
    result = ReservasService(db).get_reserva_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    
    ReservasService(db).update_reserva(id, reservas)
    return JSONResponse(status_code=200, content={"message": "Se modifico la reserva"})


@reservas_router.delete('/reservas/{id}', tags=['Reservas'], response_model=dict, status_code=200)
def delete_reservas(id: int, db = Depends(get_database_session))-> dict:
    #db = Session()
    result: ReservasModel = db.query(ReservasModel).filter(ReservasModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontró"})
    ReservasService(db).delete_reserva(id)
    return JSONResponse(status_code=200, content={"message": "Se elimino la reserva"})