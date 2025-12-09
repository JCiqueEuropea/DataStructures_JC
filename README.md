📦 Data Structures API
======================

![alt text](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![alt text](https://img.shields.io/badge/FastAPI-0.109%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)

![alt text](https://img.shields.io/badge/SQL_Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)
![alt text](https://img.shields.io/badge/SQLAlchemy-Alembic-red?style=for-the-badge)

![alt text](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![alt text](https://img.shields.io/badge/Tests-Pytest-yellow?style=for-the-badge)

Una API RESTful de alto rendimiento diseñada para demostrar la implementación de **Estructuras de Datos Avanzadas** (
Árboles Binarios de Búsqueda y Listas Enlazadas) en un entorno de desarrollo moderno con persistencia en **SQL Server**.

🚀 Características Principales
------------------------------

* **Estructuras de Datos Híbridas:** Implementación de **BST (Binary Search Tree)** para la búsqueda eficiente de
  productos
  y **Listas Enlazadas** para la gestión de pedidos en memoria.
* **Persistencia Robusta:** Integración con **SQL Server** mediante SQLAlchemy para asegurar la integridad de los datos
  a
  largo plazo.
* **Lazy Loading (Carga Perezosa):** Estrategia inteligente de caché. Los datos no se cargan masivamente al inicio (
  evitando "Cold Start"), sino que se recuperan de SQL Server y se almacenan en las estructuras de memoria solo cuando
  son solicitados.
* **Validación Estricta:** Uso de Pydantic V2 para sanitización automática de entradas y reglas de negocio complejas.
* **Seguridad:** Autenticación mediante **API Key** en headers.
* **Migraciones Automáticas:** Gestión del esquema de base de datos mediante **Alembic** (Code-First).
* **Arquitectura Limpia:** Separación estricta de responsabilidades (Routes, Services, Models, Data Store).

🛠️ Stack Tecnológico
---------------------

* **Framework:** FastAPI
* **Base de Datos:** Microsoft SQL Server
* **ORM:** SQLAlchemy
* **Migraciones:** Alembic
* **Validación:** Pydantic V2
* **Testing:** Pytest & HTTP Client
* **Config:** Pydantic Settings (.env)

🗄️ Decisiones de Arquitectura
------------------------------

### 1\. SQL Server vs MySQL

Se ha optado por **Microsoft SQL Server** aprovechando su integración nativa en entornos empresariales .NET y su
disponibilidad en el entorno de desarrollo actual. A nivel de ORM (SQLAlchemy), el cambio entre SQL Server y MySQL es
transparente, diferenciándose principalmente en el driver de conexión (`pyodbc` vs `pymysql`) y ciertos dialectos de
SQL (
ej.
paginación o tipos de datos específicos), pero la lógica de negocio permanece agnóstica.

### 2\. Lazy Loading

En lugar de cargar toda la base de datos en las estructuras de memoria al arrancar la aplicación (lo cual sería
ineficiente y lento), implementamos **Lazy Loading**:

* Al pedir un producto, primero se busca en el **BST**.
* Si no está, se consulta a SQL Server, se inserta en el BST y se devuelve.
* Las siguientes peticiones son servidas instantáneamente desde la memoria RAM.

### 3\. Settings con Caché

Utilizamos el decorador `@lru_cache()` en `Settings.py`. Esto garantiza que el archivo `.env` se lea una sola vez al
iniciar,
y las siguientes llamadas a la configuración sean inmediatas, mejorando el rendimiento global.

📦 Estructura del Proyecto
--------------------------

```
.
├── alembic            # Scripts de migración de base de datos
├── app
│   ├── database       # Configuración de conexión a SQL Server
│   ├── models         # Modelos SQL (SQLAlchemy) y Esquemas (Pydantic)
│   ├── routes         # Endpoints de la API (Controllers)
│   ├── services       # Lógica de negocio y gestión de estructuras (BST/Listas)
│   ├── errors.py      # Excepciones personalizadas
│   └── settings.py    # Configuración de entorno con caché
├── tests              # Tests automáticos (Pytest) y manuales (.http)
├── .env               # Variables de entorno (No sube al repo)
├── alembic.ini        # Configuración de Alembic
├── main.py            # Punto de entrada y gestión de ciclo de vida
└── requirements.txt   # Dependencias
```

⚙️ Instalación y Configuración
------------------------------

### 1\. Prerrequisitos

* Python 3.10+
* SQL Server instalado y en ejecución.
* Driver ODBC 17 for SQL Server.

### 2\. Clonar el repositorio

```
git clone https://github.com/tu-usuario/DataStructures_JC.git
cd DataStructures_JC
```

### 3\. Crear entorno virtual

```
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate  
```

### 4\. Instalar dependencias

```
pip install -r requirements.txt
```

### 5\. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

``` 
# Ejemplo para conexión Windows Auth (Trusted Connection)  
DB_CONNECTION_STRING="mssql+pyodbc://LOCALHOST\SQLEXPRESS/DataStructuresDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
API_KEY_SECRET="mi_super_secreto_api_key_123"  
ENVIRONMENT="development"
LOG_LEVEL="INFO"   
```

### 6\. Base de Datos y Migraciones (Alembic)

El proyecto usa Alembic para gestionar el esquema.

**Automático:** Al iniciar la aplicación (`main.py`), el sistema ejecuta automáticamente las migraciones pendientes.

**Manual (Comandos útiles):**

```
# Crear una nueva migración tras cambiar modelos  
alembic revision --autogenerate -m "Descripción del cambio" 
 
# Aplicar cambios a la BD  
alembic upgrade head  
```

▶️ Ejecución
------------

Levanta el servidor de desarrollo:

```
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

La API estará disponible en: http://127.0.0.1:8000

📖 Documentación de la API
--------------------------

FastAPI genera documentación interactiva automáticamente. Una vez iniciada la app, visita:

* **Swagger UI:** [http://127.0.0.1:8000/docs](https://www.google.com/url?sa=E&q=http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](https://www.google.com/url?sa=E&q=http://127.0.0.1:8000/redoc)

🛡️ Reglas de Negocio y Validaciones
------------------------------------

Gracias a Pydantic V2, implementamos validaciones robustas antes de llegar a la capa de lógica:

1. **Sanitización Automática:**
    * Input:`name: " teclado gamer "`
    * Output:`Teclado Gamer` (Trimmed & Title Case).
2. **Integridad de Datos:**
    * Precios > 0.
    * Pedidos deben contener al menos 1 producto.
3. **Lógica de Colecciones:**
    * Input Erróneo:`[{id:1, qty:2}, {id:1, qty:5}]`
    * Resultado:`422 Validation Error` (No se permiten duplicados, se fuerza la consolidación).

🧪 Testing
----------

### Tests Automáticos (Pytest)

Se utiliza **SQLite en Memoria** para aislar los tests de la base de datos real de SQL Server.

````
pytest -v
````

_Cobertura:_ Creación, lectura, actualización, borrado, validaciones de errores y autenticación.

### Tests Manuales (.http)

Se incluye el archivo tests/api_tests.http para probar endpoints directamente desde VS Code o PyCharm sin necesidad de
Postman.

📝 Licencia
-----------

Este proyecto está bajo la Licencia MIT. Siéntete libre de usarlo y modificarlo.
___
Hecho con ❤️ y 🐍 Python para la Universidad Europea