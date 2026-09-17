# API de Gestion de Libros con FastAPI y SQLite

Este proyecto contiene una API REST didactica para gestionar libros utilizando **FastAPI**, **SQLAlchemy** y **SQLite**. La aplicacion esta organizada por capas para separar la configuracion, el acceso a datos, los modelos, los esquemas, los controladores y las rutas HTTP.

El objetivo de esta guia es explicar el proyecto tal y como se ha construido, paso a paso. El codigo fuente esta escrito en ingles y esta documentacion en espanol.

## Indice

1. [Arquitectura y estructura](#arquitectura-y-estructura)
2. [Requisitos previos](#requisitos-previos)
3. [Instalacion paso a paso](#instalacion-paso-a-paso)
4. [Construccion del proyecto](#construccion-del-proyecto)
5. [Arrancar el servidor](#arrancar-el-servidor)
6. [Probar la API con Swagger](#probar-la-api-con-swagger)
7. [Endpoints implementados](#endpoints-implementados)
8. [Ejemplos de peticiones y respuestas](#ejemplos-de-peticiones-y-respuestas)
9. [Estado actual y siguientes pasos](#estado-actual-y-siguientes-pasos)
10. [Resolucion de problemas](#resolucion-de-problemas)

## Arquitectura y estructura

La estructura actual del proyecto es la siguiente:

```text
fastapi-api/
|
├── config/
│   ├── __init__.py
│   └── config_variables.py   # Variables de entorno y configuracion
├── controller/
│   ├── __init__.py
│   └── book_controller.py     # Logica de acceso a datos de libros
├── database/
│   ├── __init__.py
│   └── database.py            # Motor, sesiones y dependencia de BD
├── model/
│   ├── __init__.py
│   └── book_model.py          # Modelo ORM de la tabla book
├── routes/
│   ├── __init__.py
│   └── routes.py               # Endpoints HTTP de libros
├── schema/
│   ├── __init__.py
│   └── book_schema.py          # Validacion y serializacion Pydantic
├── .env                        # Configuracion local
├── .env.example                # Plantilla de configuracion
├── db.sqlite3                  # Base de datos SQLite local
├── main.py                     # Punto de entrada de FastAPI
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Documentacion
```

### Flujo de una peticion

1. El cliente envia una peticion HTTP a una ruta definida en `routes/routes.py`.
2. FastAPI valida el cuerpo y los parametros mediante los esquemas de `schema/book_schema.py`.
3. La dependencia `get_db()` abre una sesion SQLAlchemy para esa peticion.
4. La ruta delega la operacion al controlador de `controller/book_controller.py`.
5. El controlador utiliza el modelo `Book` para consultar o guardar datos en SQLite.
6. SQLAlchemy devuelve el resultado y Pydantic lo serializa como JSON.
7. La sesion se cierra al finalizar la peticion.

## Requisitos previos

Antes de comenzar, necesitas:

- Python 3.10 o superior.
- `pip`.
- Un editor de codigo, por ejemplo VS Code.

Puedes comprobar las versiones instaladas con:

```bash
python3 --version
pip --version
```

## Instalacion paso a paso

### Paso 1: Situarse en el proyecto

Desde una terminal, entra en la carpeta que contiene `main.py`:

```bash
cd /ruta/hacia/fastapi-api
```

### Paso 2: Crear el entorno virtual

El entorno virtual mantiene aisladas las dependencias de este proyecto:

```bash
python3 -m venv .venv
```

En Windows se puede utilizar:

```powershell
python -m venv .venv
```

### Paso 3: Activar el entorno virtual

En macOS o Linux:

```bash
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

En Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

Cuando se activa correctamente, suele aparecer `(.venv)` al comienzo de la linea de la terminal.

### Paso 4: Instalar las dependencias

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

Las dependencias principales son:

- `fastapi`: framework para construir la API REST.
- `uvicorn`: servidor ASGI que ejecuta FastAPI.
- `sqlalchemy`: ORM para trabajar con SQLite mediante modelos Python.
- `pydantic`: validacion de los datos de entrada y salida.
- `python-dotenv`: lectura de variables desde `.env`.

SQLite no se instala con `pip`: forma parte de la libreria estandar de Python y la base de datos se almacena en el archivo local `db.sqlite3`.

### Paso 5: Configurar las variables de entorno

El archivo `.env` actual contiene:

```env
APP_TITLE="Library"
APP_VERSION="0.0.1"
APP_DESCRIPTION="app de una librería"
DATABASE_NAME="db.sqlite3"
DATABASE_URL="sqlite:///./db.sqlite3"
```

El archivo `.env.example` existe como plantilla, aunque actualmente esta vacio. Si se parte de un clonado nuevo y el archivo `.env` no existe, se puede crear con:

```bash
cp .env.example .env
```

Despues hay que anadir las variables anteriores al archivo `.env`, o dejar que `config/config_variables.py` utilice sus valores por defecto. Si una variable no existe, la aplicacion utiliza ese valor alternativo.

## Construccion del proyecto

La aplicacion se construyo siguiendo el orden de sus dependencias: primero la configuracion, despues la base de datos, el modelo, los esquemas, el controlador, las rutas y finalmente el punto de entrada.

### Paso 1: Configuracion (`config/config_variables.py`)

Este modulo carga el archivo `.env` y centraliza los valores que necesita la aplicacion:

```python
import os
from dotenv import load_dotenv

load_dotenv()

APP_TITLE: str = os.getenv("APP_TITLE", "Library")
APP_VERSION: str = os.getenv("APP_VERSION", "0.0.1")
APP_DESCRIPTION: str = os.getenv(
    "APP_DESCRIPTION",
    "app de una librería"
)

DATABASE_NAME: str = os.getenv("DATABASE_NAME", "db.sqlite3")
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
```

`load_dotenv()` busca las variables definidas en `.env`. `os.getenv()` permite usar un valor alternativo cuando una variable no esta definida.

### Paso 2: Conexion y sesiones (`database/database.py`)

SQLAlchemy necesita un motor y una fabrica de sesiones para comunicarse con SQLite:

```python
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from config.config_variables import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()
```

La opcion `check_same_thread=False` permite utilizar SQLite en el contexto de peticiones gestionadas por FastAPI. `SessionLocal` crea sesiones sin confirmar automaticamente las transacciones, por lo que el controlador decide cuando hacer `commit()`.

La dependencia `get_db()` entrega una sesion a cada ruta y la cierra siempre:

```python
def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

El bloque `finally` evita dejar sesiones abiertas despues de una peticion.

### Paso 3: Modelo ORM (`model/book_model.py`)

El modelo `Book` representa la tabla `book` de SQLite:

```python
from sqlalchemy import Column, Integer, String, Boolean
from database.database import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(150), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    pages = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
```

Los campos son:

- `id`: identificador entero, clave primaria y autoincremental.
- `title`: titulo obligatorio de hasta 150 caracteres.
- `author`: autor obligatorio de hasta 100 caracteres.
- `pages`: numero de paginas almacenado como entero.
- `is_available`: indica si el libro esta disponible; por defecto es `True`.

Los indices de `title`, `author` e `id` ayudan a localizar registros con mayor rapidez.

### Paso 4: Esquemas Pydantic (`schema/book_schema.py`)

Los esquemas definen los datos que entran y salen de la API. Son diferentes del modelo ORM: el modelo describe la tabla y Pydantic describe el JSON.

El esquema comun `BookBase` valida los datos basicos:

```python
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    author: str = Field(..., min_length=1, max_length=100)
    pages: Optional[int] = Field(None, gt=0)
    is_available: bool = Field(default=True)
```

`BookCreate` hereda esos campos y se utiliza en `POST /book/`. El identificador no se envia porque lo genera SQLite.

`BookResponse` anade el campo `id` y utiliza:

```python
model_config = ConfigDict(from_attributes=True)
```

Esto permite que Pydantic convierta directamente un objeto SQLAlchemy en la respuesta JSON.

El proyecto tambien contiene `BookUpdate` como preparacion para futuras actualizaciones. Actualmente no esta conectado a ninguna ruta y, por tanto, no se puede utilizar desde la API.

### Paso 5: Controlador (`controller/book_controller.py`)

El controlador concentra las operaciones de base de datos para que las rutas no tengan que contener consultas SQLAlchemy directamente.

#### Obtener libros

```python
def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    try:
        return db.query(Book).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating book {str(error)}"
        )
```

`skip` permite saltar registros y `limit` limita el numero de resultados.

#### Crear libros

```python
def create_book(db: Session, book_data: BookCreate) -> Book:
    new_book = Book(
        title=book_data.title,
        author=book_data.author,
        pages=book_data.pages,
        is_available=book_data.is_available
    )

    try:
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error in creating book {str(error)}"
        )
```

El flujo es:

1. Se construye un objeto `Book` con los datos validados.
2. `db.add()` lo anade a la sesion.
3. `db.commit()` guarda la transaccion en SQLite.
4. `db.refresh()` recupera el `id` generado.
5. Si ocurre un error, `db.rollback()` revierte la transaccion.

### Paso 6: Rutas (`routes/routes.py`)

El router utiliza el prefijo `/book` y agrupa sus operaciones con la etiqueta `Book` en Swagger:

```python
router = APIRouter(
    prefix="/book",
    tags=["Book"]
)
```

La ruta de listado valida `skip` y `limit` mediante `Query` y obtiene una sesion mediante `Depends(get_db)`:

```python
@router.get("/", response_model=List[BookResponse])
def read_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return controller.get_all(db=db, skip=skip, limit=limit)
```

La ruta de creacion recibe un `BookCreate`, delega en el controlador y devuelve `201 Created`:

```python
@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_book(
    book_data: BookCreate,
    db: Session = Depends(get_db)
):
    return controller.create_book(db=db, book_data=book_data)
```

### Paso 7: Aplicacion principal (`main.py`)

`main.py` ensambla todos los modulos:

```python
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    lifespan=lifespan
)
```

Antes de aceptar peticiones, el ciclo de vida crea las tablas que todavia no existen:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
```

Por eso la tabla `book` se crea automaticamente al arrancar el servidor.

Tambien se configura CORS para permitir que un frontend independiente pueda consumir la API:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

Finalmente, `app.include_router(books_router)` registra las rutas de libros y la ruta raiz `GET /` permite comprobar el estado de la aplicacion.

## Arrancar el servidor

Con el entorno virtual activado, ejecuta:

```bash
uvicorn main:app --reload
```

Los elementos del comando son:

- `main`: archivo que contiene la aplicacion.
- `app`: instancia de `FastAPI` dentro de `main.py`.
- `--reload`: reinicia el servidor cuando se modifica el codigo.

Direcciones disponibles:

- API: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

Al arrancar por primera vez, se crea o actualiza `db.sqlite3` y se registra la tabla `book`.

Para detener el servidor, pulsa `Ctrl+C` en la terminal donde esta ejecutando Uvicorn.

## Probar la API con Swagger

1. Arranca el servidor con `uvicorn main:app --reload`.
2. Abre <http://127.0.0.1:8000/docs>.
3. Selecciona un endpoint.
4. Pulsa **Try it out**.
5. Completa los parametros o el cuerpo JSON.
6. Pulsa **Execute**.

Tambien puedes consultar la documentacion alternativa en <http://127.0.0.1:8000/redoc>.

## Endpoints implementados

| Metodo | Ruta | Descripcion | Respuesta principal |
| --- | --- | --- | --- |
| `GET` | `/` | Comprueba que la API esta activa | `200 OK` |
| `GET` | `/book/` | Lista libros con paginacion | `200 OK` |
| `POST` | `/book/` | Crea un libro | `201 Created` |

La paginacion de `GET /book/` acepta:

- `skip`: registros que se omiten. Valor inicial `0`, minimo `0`.
- `limit`: maximo de registros. Valor inicial `100`, entre `1` y `100`.

Actualmente no existen rutas `GET /book/{id}`, `PUT`, `PATCH` ni `DELETE`.

## Ejemplos de peticiones y respuestas

### 1. Comprobar el estado de la API

Peticion:

```bash
curl http://127.0.0.1:8000/
```

Respuesta:

```json
{
  "status": "online",
  "message": "Welcome to Library",
  "docs_url": "/docs",
  "redoc_url": "/redoc"
}
```

### 2. Listar libros

Peticion:

```bash
curl "http://127.0.0.1:8000/book/?skip=0&limit=10"
```

Si no hay registros, la respuesta es:

```json
[]
```

Cuando existen libros, la respuesta tiene este formato:

```json
[
  {
    "title": "Don Quijote",
    "author": "Miguel de Cervantes",
    "pages": 850,
    "is_available": true,
    "id": 1
  }
]
```

### 3. Crear un libro

Peticion:

```bash
curl -X POST "http://127.0.0.1:8000/book/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Don Quijote",
    "author": "Miguel de Cervantes",
    "pages": 850,
    "is_available": true
  }'
```

Respuesta esperada, con codigo `201 Created`:

```json
{
  "title": "Don Quijote",
  "author": "Miguel de Cervantes",
  "pages": 850,
  "is_available": true,
  "id": 1
}
```

El campo `is_available` es opcional porque tiene el valor `true` por defecto. `title` y `author` son obligatorios. `pages`, cuando se envia, debe ser mayor que cero.

### 4. Validacion de datos

Por ejemplo, esta peticion no es valida porque `pages` no puede ser negativo:

```bash
curl -X POST "http://127.0.0.1:8000/book/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Libro de prueba",
    "author": "Autor de prueba",
    "pages": -1
  }'
```

FastAPI devuelve un error `422 Unprocessable Entity` generado por Pydantic.

## Estado actual y siguientes pasos

La version actual ya permite:

- Cargar configuracion desde `.env`.
- Crear automaticamente la tabla `book` al iniciar.
- Abrir y cerrar sesiones SQLAlchemy por peticion.
- Listar libros con `GET /book/`.
- Crear libros con `POST /book/`.
- Validar los datos recibidos con Pydantic.
- Generar documentacion interactiva con Swagger y ReDoc.
- Permitir peticiones desde un frontend mediante CORS.

Como siguientes pasos del proyecto se pueden implementar:

- Consultar un libro por identificador con `GET /book/{book_id}`.
- Completar el esquema `BookUpdate` y anadir `PUT` o `PATCH`.
- Anadir la eliminacion con `DELETE /book/{book_id}`.
- Corregir los nombres `page` e `is_avaible` del esquema de actualizacion para que coincidan con `pages` e `is_available`.
- Anadir tests automatizados para las rutas y el controlador.
- Restringir `allow_origins` a los dominios reales del frontend en produccion.
- Utilizar migraciones, por ejemplo Alembic, cuando cambie el modelo de datos.

## Resolucion de problemas

### `ModuleNotFoundError: No module named 'fastapi'`

Activa el entorno virtual y vuelve a instalar las dependencias:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### El comando `uvicorn` no se encuentra

Comprueba que el entorno virtual esta activado. Tambien puedes arrancar el servidor mediante el interprete de Python:

```bash
python -m uvicorn main:app --reload
```

### La API no muestra los libros

Comprueba que estas utilizando el prefijo correcto: `/book/`, en singular. Tambien puedes inspeccionar el archivo `db.sqlite3` con una extension de VS Code para SQLite o con DB Browser for SQLite.

### Reiniciar la base de datos

Deten el servidor, elimina `db.sqlite3` y vuelve a arrancarlo:

```bash
rm db.sqlite3
uvicorn main:app --reload
```

La tabla `book` se creara de nuevo durante el inicio de FastAPI.
