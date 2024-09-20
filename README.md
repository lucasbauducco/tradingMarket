# Trading Project

## Resumen del Proyecto

Este es un proyecto de Django diseñado para realizar análisis y gestión de trading, enfocado en la implementación de un sistema que interactúa con datos de acciones. Utiliza `Django` para la estructura web y `Celery` para la programación de tareas asíncronas, como la actualización periódica de datos de acciones (CEDears).

## Estructura del Proyecto

```plaintext
trading/
│
├── analysisActions/          # Aplicación principal para análisis de acciones
│   ├── migrations/           # Migraciones de la base de datos
│   ├── tasks.py              # Definición de tareas de Celery
│   └── models.py             # Modelos de datos
│
├── trading/                  # Configuración principal del proyecto
│   ├── settings.py           # Configuración de Django
│   ├── urls.py               # Rutas de la aplicación
│   └── wsgi.py               # Interfaz WSGI para el servidor
│
└── manage.py                 # Herramienta de administración de Django
```
## Configuración del Entorno

### 1. Clonar el Repositorio

```bash
git clone <URL del repositorio>
cd <nombre del proyecto>
```
## Configuración del Entorno

### 2. Crear un Entorno Virtual

```bash
python -m venv venv
```
### 3. Activar el Entorno Virtual

#### En Windows:

```bash
venv\Scripts\activate
```
#### En macOS/Linux:
```bash
source venv/bin/activate
```
### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```
## Configuración de Celery

### Dependencias

Este proyecto utiliza Redis como broker de mensajes. Asegúrate de tener Redis instalado y en funcionamiento.

```bash
redis-server
```
## Variables de Entorno

Configura el `SECRET_KEY` y otros parámetros sensibles en un archivo `.env` para mantener la seguridad del proyecto.

## Migraciones de Base de Datos

Ejecuta las migraciones iniciales para configurar la base de datos.

```bash
python manage.py migrate
```
## Ejecución del Servidor

Para iniciar el servidor de desarrollo, utiliza el siguiente comando:

```bash
python manage.py runserver
```
## Ejecución de Celery

Para ejecutar las tareas de Celery, abre otra terminal, activa el entorno virtual y ejecuta:

### 1. Worker de Celery

```bash
celery -A trading worker --loglevel=info
```
### 2. Scheduler de Celery (Beat)

```bash
celery -A trading beat --loglevel=info
```
## Contribuciones

Las contribuciones son bienvenidas. Abre un issue o envía un pull request para discutir cambios o mejoras.

## Licencia

Este proyecto está bajo la Licencia MIT. La licencia es de mi autoría. Consulta el archivo LICENSE para más detalles.

