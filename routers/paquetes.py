from fastapi import APIRouter, status, HTTPException
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import get_database_session
from models.paquetes import Paquetes as PaquetesModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.paquetes import PaquetesService
from schemas.paquetes import Paquetes, PaqueteRespuesta

paquetes_router = APIRouter()

@paquetes_router.get('/paquetes', tags=['Paquetes'], response_model=List[PaqueteRespuesta],
                     status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_paquetes(db=Depends(get_database_session)) -> List[PaqueteRespuesta]:
    result = PaquetesService(db).get_paquetes()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron paquetes")
    return result


@paquetes_router.get('/paquetes/{id}', tags=['Paquetes'], response_model=PaqueteRespuesta, dependencies=[Depends(JWTBearer())])
def get_paquetexId(id: int = Path(ge=1, le=2000), db=Depends(get_database_session)) -> PaqueteRespuesta:
    result = PaquetesService(db).get_paquete_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paquete no encontrado")
    return result


@paquetes_router.post('/paquetes', tags=['Paquetes'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_paquete(paquete: Paquetes,  db=Depends(get_database_session)) -> dict:
    PaquetesService(db).create_paquete(paquete)
    return JSONResponse(status_code=201, content={"message": "Se registro el paquete"})


@paquetes_router.put('/paquetes/{id}', tags=['Paquetes'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_paquete(id: int, paquete: Paquetes,  db = Depends(get_database_session))-> dict:
    result = PaquetesService(db).get_paquete_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})

    PaquetesService(db).update_paquete(id, paquete)
    return JSONResponse(status_code=200, content={"message": "Se modifico el paquete"})


@paquetes_router.delete('/paquetes/{id}', tags=['Paquetes'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_paquete(id: int,  db = Depends(get_database_session))-> dict:
    #db = Session()
    result: PaquetesModel = db.query(PaquetesModel).filter(PaquetesModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontró"})
    PaquetesService(db).delete_paquete(id)
    return JSONResponse(status_code=200, content={"message": "Se elimino el paquete"})