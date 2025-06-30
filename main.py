from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from starlette.middleware.cors import CORSMiddleware
from routers.destinos import destinos_router
from routers.usuarios import usuarios_router
from routers.paquetes import paquetes_router
from routers.reservas import reservas_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.title = "Agencia de Viajes"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_router)
app.include_router(destinos_router)
app.include_router(paquetes_router)
app.include_router(reservas_router)

Base.metadata.create_all(bind=engine)

# 1. Servimos todos los archivos estáticos del directorio frontend en la ruta "/" (raíz)
# app.mount("/", StaticFiles(directory="frontend", html=True ), name="frontend")


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Agencia de Viajes</h1>')