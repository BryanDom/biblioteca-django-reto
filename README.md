# Sistema de Gestion de Biblioteca

Sistema web desarrollado con Django para la administracion de autores, libros, usuarios y prestamos de una biblioteca. Incluye panel de administracion avanzado, API REST con autenticacion por token y documentacion  generada automaticamente con Swagger y ReDoc.

---

## Tabla de Contenidos

1. [Tecnologias utilizadas](#tecnologias-utilizadas)
2. [Requisitos previos](#requisitos-previos)
3. [Instalacion](#instalacion)
4. [Crear el superusuario](#crear-el-superusuario)
5. [Ejecutar el proyecto](#ejecutar-el-proyecto)
6. [Endpoints de la API](#endpoints-de-la-api)
7. [Autenticacion por Token](#autenticacion-por-token)
8. [Estructura del proyecto](#estructura-del-proyecto)
9. [Funcionalidades principales](#funcionalidades-principales)

---

## Tecnologias utilizadas

| Tecnologia | Version | Proposito |
|---|---|---|
| Python | 3.x | Lenguaje base |
| Django | 6.0.5 | Framework web principal |
| Django REST Framework | 3.17.1 | Construccion de la API REST |
| drf-yasg | 1.21.15 | Documentacion automatica OpenAPI / Swagger |
| django-import-export | 4.4.1 | Importacion y exportacion de datos en el Admin |
| Bootstrap 5 | 5.x | Framework CSS para la interfaz web |
| Bootstrap Icons | — | Iconografia en la interfaz web |
| SQLite | — | Base de datos por defecto de Django |

---

## Requisitos previos

Antes de instalar el proyecto, asegurese de tener instalado lo siguiente:

- **Python 3.10 o superior** — [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **pip** — incluido en la instalacion de Python
- **Git** — [https://git-scm.com/](https://git-scm.com/)

---

## Instalacion

Siga los pasos a continuacion para configurar el entorno de desarrollo local.

### 1. Clonar el repositorio

```bash
git clone https://github.com/BryanDom/biblioteca-django-reto.git
cd biblioteca-django-reto
```

### 2. Crear y activar el entorno virtual

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

> **Nota:** Bootstrap 5 y Bootstrap Icons ya se encuentran incluidos en la carpeta `static/` del repositorio. No es necesario descargarlos ni instalarlos por separado.

### 4. Aplicar las migraciones

```bash
python manage.py migrate
```

## Crear el superusuario

Para acceder al panel de administracion de Django, es necesario crear un superusuario:

```bash
python manage.py createsuperuser
```

El sistema solicitara un nombre de usuario, correo electronico y contrasena.

---

## Ejecutar el proyecto

```bash
python manage.py runserver
```

Una vez iniciado, el proyecto estara disponible en las siguientes direcciones:

| Interfaz | URL |
|---|---|
| Sitio web (CRUD de Prestamos) | http://127.0.0.1:8000/ |
| Panel de administracion | http://127.0.0.1:8000/admin/ |
| Documentacion Swagger | http://127.0.0.1:8000/api/docs/ |
| Documentacion ReDoc | http://127.0.0.1:8000/api/redoc/ |

---

## Endpoints de la API

Todos los endpoints requieren autenticacion mediante token, excepto la obtencion del token.

### Autores

| Metodo | Endpoint | Descripcion |
|---|---|---|
| `GET` | `/api/autores/` | Listar todos los autores |
| `POST` | `/api/autores/` | Crear un nuevo autor |
| `GET` | `/api/autores/{id}/` | Obtener un autor por ID |
| `PUT` | `/api/autores/{id}/` | Actualizar un autor completo |
| `PATCH` | `/api/autores/{id}/` | Actualizar campos de un autor |
| `DELETE` | `/api/autores/{id}/` | Eliminar un autor |

### Libros

| Metodo | Endpoint | Descripcion |
|---|---|---|
| `GET` | `/api/libros/` | Listar todos los libros |
| `POST` | `/api/libros/` | Crear un nuevo libro |
| `GET` | `/api/libros/{id}/` | Obtener un libro por ID |
| `PUT` | `/api/libros/{id}/` | Actualizar un libro completo |
| `PATCH` | `/api/libros/{id}/` | Actualizar campos de un libro |
| `DELETE` | `/api/libros/{id}/` | Eliminar un libro |

### Usuarios

| Metodo | Endpoint | Descripcion |
|---|---|---|
| `GET` | `/api/usuarios/` | Listar todos los usuarios |
| `POST` | `/api/usuarios/` | Crear un nuevo usuario |
| `GET` | `/api/usuarios/{id}/` | Obtener un usuario por ID |
| `PUT` | `/api/usuarios/{id}/` | Actualizar un usuario completo |
| `PATCH` | `/api/usuarios/{id}/` | Actualizar campos de un usuario |
| `DELETE` | `/api/usuarios/{id}/` | Eliminar un usuario |

### Prestamos

| Metodo | Endpoint | Descripcion |
|---|---|---|
| `GET` | `/api/prestamos/` | Listar todos los prestamos |
| `POST` | `/api/prestamos/` | Registrar un nuevo prestamo |
| `GET` | `/api/prestamos/{id}/` | Obtener un prestamo por ID |
| `PUT` | `/api/prestamos/{id}/` | Actualizar un prestamo completo |
| `PATCH` | `/api/prestamos/{id}/` | Actualizar campos de un prestamo |
| `DELETE` | `/api/prestamos/{id}/` | Eliminar un prestamo |

### Autenticacion

| Metodo | Endpoint | Descripcion |
|---|---|---|
| `POST` | `/api/token/` | Obtener token de acceso |

---

## Autenticacion por Token

La API utiliza autenticacion por token (Token Authentication de DRF).

### Paso 1: Obtener el token

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -d "username=admin&password=tu_contrasena"
```

Respuesta:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Paso 2: Usar el token en las peticiones

Incluya el token en el encabezado `Authorization` de cada solicitud:

```bash
curl http://127.0.0.1:8000/api/autores/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

---

## Estructura del proyecto

```
biblioteca-django-reto/
|
+-- biblioteca/                         # App principal del proyecto
|   +-- migrations/                     # Migraciones de la base de datos
|   +-- admin.py                        # Configuracion del panel de administracion
|   +-- apps.py
|   +-- forms.py                        # Formularios Django para la interfaz web
|   +-- models.py                       # Modelos: Autor, Libro, Usuario, Prestamo
|   +-- serializers.py                  # Serializadores de la API REST
|   +-- views.py                        # Vistas de la API y de las plantillas web
|
+-- config/                             # Configuracion del proyecto Django
|   +-- settings.py
|   +-- urls.py                         # Rutas principales (admin, API, Swagger, web)
|   +-- asgi.py
|   +-- wsgi.py
|
+-- static/                             # Archivos estaticos
|   +-- css/                            # Bootstrap 5 (incluido en el repositorio)
|   +-- js/                             # Bootstrap JS (incluido en el repositorio)
|
+-- templates/                          # Plantillas HTML con Django Templates
|   +-- base.html                       # Plantilla base
|   +-- prestamos/
|       +-- lista.html
|       +-- formulario.html
|       +-- confirmar_eliminar.html
|
+-- db.sqlite3                          # Base de datos SQLite
+-- manage.py                           # CLI de Django
+-- requirements.txt                    # Dependencias del proyecto
+-- README.md
```

---

## Funcionalidades principales

### Panel de administracion de Django

- Registro de los modelos Autor, Libro, Usuario y Prestamo.
- Filtros laterales y busqueda por campos relevantes en cada modelo.
- Importacion y exportacion de datos en formatos CSV, XLSX y JSON mediante `django-import-export`.

### API REST

- CRUD completo para los cuatro modelos expuesto a traves de `DefaultRouter` de DRF.
- Autenticacion por Token para proteger todos los endpoints.
- Documentacion interactiva generada automaticamente disponible en `/api/docs/` (Swagger UI) y `/api/redoc/` (ReDoc).

### Interfaz web de Prestamos

- Listado de prestamos con indicador de estado (activo / devuelto).
- Formulario para registrar y editar prestamos.
- Confirmacion de eliminacion antes de borrar un registro.
- Interfaz construida con Django Templates y Bootstrap 5.
