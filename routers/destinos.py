from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import get_database_session
from models.destinos import Destinos as DestinosModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.destinos import DestinosService
from schemas.destinos import Destinos

destinos_router = APIRouter()

@destinos_router.get('/destinos', tags=['Destinos'], response_model=List[Destinos], status_code=200, dependencies=[Depends(JWTBearer())])
def get_destinos(db = Depends(get_database_session)) -> List[Destinos]:
    #db = Session()
    result = DestinosService(db).get_destinos()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@destinos_router.get('/destinos/{id}', tags=['Destinos'], response_model=Destinos)
def get_destinos(id: int = Path(ge=1, le=2000), db = Depends(get_database_session)) -> Destinos:
    #db = Session()
    result = DestinosService(db).get_destino_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@destinos_router.post('/destinos', tags=['Destinos'], response_model=dict, status_code=201)
def create_destinos(destino: Destinos, db = Depends(get_database_session)) -> dict:
    #db = Session()
    DestinosService(db).create_destino(destino)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el destino"})


@destinos_router.put('/destinos/{id}', tags=['Destinos'], response_model=dict, status_code=200)
def update_destino(id: int, destino: Destinos, db = Depends(get_database_session))-> dict:
    #db = Session()
    result = DestinosService(db).get_destino_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    
    DestinosService(db).update_producto(id, destino)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el destino"})


@destinos_router.delete('/destinos/{id}', tags=['Destinos'], response_model=dict, status_code=200)
def delete_destino(id: int, db = Depends(get_database_session))-> dict:
    #db = Session()
    result: DestinosModel = db.query(DestinosModel).filter(DestinosModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontró"})
    DestinosService(db).delete_producto(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el destino"})