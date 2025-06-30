from fastapi import APIRouter, status, Depends, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional, List
from config.database import get_database_session
from models.destinos import Destinos as DestinosModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.destinos import DestinosService
from services.paquetes import PaquetesService
from schemas.destinos import Destinos
from schemas.paquetes import Paquetes

destinos_router = APIRouter()

@destinos_router.get('/destinos', tags=['Destinos'], response_model=List[Destinos],
                     status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_destinos(
    nombre: Optional[str] = Query(None),
    pais: Optional[str] = Query(None),
    db=Depends(get_database_session)
) -> List[Destinos]:
    return DestinosService(db).get_destinos(nombre=nombre, pais=pais)


@destinos_router.get('/destinos/{id}', tags=['Destinos'], response_model=Destinos, dependencies=[Depends(JWTBearer())])
def get_destinoxId(id: int = Path(ge=1, le=2000), db = Depends(get_database_session)) -> Destinos:
    result = DestinosService(db).get_destino_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destino no encontrado")
    return result

@destinos_router.get("/destinos/{destino_id}/paquetes", tags=["Paquetes"], response_model=List[Paquetes],
                     status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_paquetes_por_destino(destino_id: int, db=Depends(get_database_session)):
    return PaquetesService(db).get_paquetes_por_destino(destino_id)


@destinos_router.post('/destinos', tags=['Destinos'], response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_destinos(destino: Destinos, db = Depends(get_database_session)) -> dict:
    DestinosService(db).create_destino(destino)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el destino"})


@destinos_router.put('/destinos/{id}', tags=['Destinos'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def update_destino(id: int, destino: Destinos, db = Depends(get_database_session))-> dict:
    result = DestinosService(db).get_destino_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    
    DestinosService(db).update_destino(id, destino)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el destino"})


@destinos_router.delete('/destinos/{id}', tags=['Destinos'], response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_destino(id: int, db = Depends(get_database_session))-> dict:
    result: DestinosModel = db.query(DestinosModel).filter(DestinosModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontró"})
    DestinosService(db).delete_destino(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el destino"})