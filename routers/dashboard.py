from fastapi import APIRouter
from fastapi import Depends
from config.database import get_database_session
from middlewares.jwt_bearer import JWTBearer
from services.dashboard import DashboardService
from schemas.dashboard import DashboardStats

dashboard_router = APIRouter()

@dashboard_router.get(
    "/dashboard/admin",
    tags=["Dashboard"],
    response_model=DashboardStats,
    dependencies=[Depends(JWTBearer())]
)
def obtener_dashboard_stats(db=Depends(get_database_session)):
    service = DashboardService(db)
    return {
        "total_destinos": service.contar_destinos(),
        "reservas_activas": service.contar_reservas_activas(),
        "usuarios_destacados": service.top_usuarios_por_reservas(),
        "paquete_mas_reservado": service.paquete_mas_reservado()
    }
