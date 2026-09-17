from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.config_variables import APP_TITLE, APP_VERSION, APP_DESCRIPTION
from database.database import Base, engine
from routes.routes import router as books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor del ciclo de vida (Lifespan).
    Crea las tablas en SQLite automáticamente al arrancar la aplicación.
    """
    # Base.metadata.create_all comprueba si la tabla 'books' existe; si no, la crea
    Base.metadata.create_all(bind=engine)
    yield
    # Lógica de cierre o limpieza (si fuera necesaria)


# Inicialización de la aplicación FastAPI
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    lifespan=lifespan
)

# Configuración de CORS (permite que el frontend independiente haga peticiones)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar el router de libros
app.include_router(books_router)


@app.get("/", tags=["Health Check"])
def read_root():
    """
    Ruta raíz para comprobar que el servidor está online y redirigir a la documentación.
    """
    return {
        "status": "online",
        "message": f"Welcome to {APP_TITLE}",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }