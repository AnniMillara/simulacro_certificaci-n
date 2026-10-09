# App Certificación

## Descripción
Aplicación web Flask con login, CRUD, categorías y protección de dueño. Sirve como base para escenarios tipo TaskTrack, Biblioteca, Películas, Comida, etc.

## Tecnologías
- Python 3.11
- Flask + Flask-Bcrypt
- MySQL + mysql-connector-python
- Jinja2

## Instalación
1. `pipenv install`
2. `pipenv shell`
3. Ejecutar `esquema.sql` en MySQL
4. Editar credenciales en `flask_app/config/mysqlconnection.py`
5. `python app.py`
6. Abrir `http://localhost:5000`

## Funcionalidades
- Registro / Login con bcrypt
- CRUD de entidades (con protección de dueño)
- CRUD de categorías
- Perfil + eliminar cuenta
- Confirmación antes de eliminar

## Rutas principales
| Método | Ruta | Acción |
|---|---|---|
| GET | / | Login |
| POST | /registro | Crear cuenta |
| POST | /login | Iniciar sesión |
| GET | /logout | Cerrar sesión |
| GET | /dashboard | Listar entidades |
| GET | /entidad/nueva | Form crear |
| POST | /entidad/crear | Guardar |
| GET | /entidad/detalle/<id> | Ver |
| GET | /entidad/editar/<id> | Form editar |
| POST | /entidad/modificar/<id> | Actualizar |
| GET | /entidad/eliminar/<id> | Borrar |
| GET | /categorias | Listar categorías |
| GET | /perfil/<id> | Ver perfil |

## Cómo adaptar a otro escenario
1. Renombrar `Entidades` → `Tareas` / `Libros` / `Platos` / etc.
2. Renombrar `entidades` → `tareas` / `libros` / `platos` en SQL.
3. Ajustar campos específicos (`fecha`, `precio`, `stock`, etc.).
4. Ajustar templates con los nombres y campos correctos.
5. Ajustar validaciones específicas del escenario.

## Qué quedó fuera y por qué
- **N:M (favoritos, inscripciones)**: se puede añadir como tabla pivote si el escenario lo pide.
- **Comentarios**: se añade como tabla extra si el escenario lo pide.
- **Filtros/búsqueda**: se pueden añadir como query params si el escenario lo pide.
- **Blueprints**: se usó un solo archivo de controladores por simplicidad.