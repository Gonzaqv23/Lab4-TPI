from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import get_database_session
from models.paquetes import Paquetes as PaquetesModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.paquetes import PaquetesService
from schemas.paquetes import Paquetes

paquetes_router = APIRouter()

@paquetes_router.get('/paquetes', tags=['Paquetes'], response_model=List[Paquetes], status_code=200 , dependencies=[Depends(JWTBearer())])
def get_paquete(db = Depends(get_database_session) ) -> List[Paquetes]:
    #db = Session()
    result = PaquetesService(db).get_paquetes()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@paquetes_router.get('/paquetes/{id}', tags=['Paquetes'], response_model=Paquetes)
def get_paquete(id: int = Path(ge=1, le=2000), db = Depends(get_database_session)) -> Paquetes:
    #db = Session()
    result = PaquetesService(db).get_paquete_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@paquetes_router.post('/paquetes', tags=['Paquetes'], response_model=dict, status_code=201)
def create_paquete(paquete: Paquetes,  db = Depends(get_database_session)) -> dict:
    #db = Session()
    PaquetesService(db).create_paquete(paquete)
    return JSONResponse(status_code=201, content={"message": "Se registro el paquete"})


@paquetes_router.put('/paquetes/{id}', tags=['Paquetes'], response_model=dict, status_code=200)
def update_paquete(id: int, paquete: Paquetes,  db = Depends(get_database_session))-> dict:
    #db = Session()
    result = PaquetesService(db).get_paquete_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})

    PaquetesService(db).update_paquete(id, paquete)
    return JSONResponse(status_code=200, content={"message": "Se modifico el paquete"})


@paquetes_router.delete('/paquetes/{id}', tags=['Paquetes'], response_model=dict, status_code=200)
def delete_paquete(id: int,  db = Depends(get_database_session))-> dict:
    #db = Session()
    result: PaquetesModel = db.query(PaquetesModel).filter(PaquetesModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontró"})
    PaquetesService(db).delete_paquete(id)
    return JSONResponse(status_code=200, content={"message": "Se elimino el paquete"})

