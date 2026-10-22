# Aplicación Web Hola Mundo con Docker Compose y MySQL

Aplicación web desarrollada en Python (Flask) que se conecta a una base de datos MySQL 8.0 gestionada y orquestada mediante Docker Compose.

---

## 📋 Requerimientos y Pasos Implementados

### a) Directorio `src/` con código fuente de la app "Hola Mundo"
Dentro del directorio `src/` se encuentran:
- **`app.py`**: Aplicación Flask que establece conexión con la base de datos MySQL, realiza una consulta de verificación (`SELECT VERSION(), NOW();`) y muestra una interfaz web amigable con el estado de la conexión. Incluye reintentos automáticos para asegurar la disponibilidad.
- **`requirements.txt`**: Dependencias de Python (`Flask`, `PyMySQL`, `cryptography`).
- **`Dockerfile`**: Imagen basada en `python:3.11-slim` para empaquetar y ejecutar la aplicación en el puerto `5000`.

### b) Archivo `docker-compose.yml`
Define y orquesta los servicios, redes, variables de entorno, volúmenes de persistencia y comprobaciones de salud (`healthcheck`).

### c) Servicio de Servidor de Aplicación (`web`)
- Construido a partir del contexto `./src`.
- Configurado con variables de entorno para conectarse dinámicamente al servicio de base de datos (`DB_HOST=db`, `DB_USER=usuario`, `DB_PASSWORD=clave123`, `DB_NAME=pruebadb`).
- Mapeo de puerto `5000:5000`.
- Dependencia condicional (`depends_on: db: condition: service_healthy`) que espera a que MySQL esté 100% listo antes de iniciar la aplicación.

### d) Servicio de Base de Datos MySQL (`db`)
- Imagen oficial `mysql:8.0`.
- Configuración de base de datos (`MYSQL_DATABASE`), usuario (`MYSQL_USER`), contraseña (`MYSQL_PASSWORD`) y contraseña de root (`MYSQL_ROOT_PASSWORD`).
- Persistencia de datos mediante el volumen nombrado `mysql_data`.
- Mapeo de puerto `3307:3306` en el host (evita conflictos con instancias locales de MySQL en el puerto 3306).
- `healthcheck` integrado con `mysqladmin ping` para monitorear el estado del servicio.

---

## 📁 Estructura del Proyecto

```text
docker-mysql-app/
│
├── docker-compose.yml       # Definición de servicios (web y db)
├── README.md                # Documentación del proyecto
└── src/
    ├── app.py               # Aplicación web Flask con conexión a MySQL
    ├── Dockerfile           # Dockerfile para la aplicación Python
    └── requirements.txt     # Dependencias de Python
```

---

## 🚀 Instrucciones de Ejecución

### 1. Iniciar los contenedores
Abre una terminal en la raíz del proyecto (`docker-mysql-app`) y ejecuta:
```bash
docker compose up -d --build
```

### 2. Probar la aplicación
- **Navegador Web:** Ingresa a [http://localhost:5000](http://localhost:5000)
- **Terminal (cURL / PowerShell):**
  ```powershell
  curl http://localhost:5000
  ```

### 3. Ver los logs de los servicios
```bash
docker compose logs -f
```

### 4. Detener los contenedores
```bash
docker compose down
```
*(Si deseas eliminar también los datos almacenados en el volumen de MySQL, ejecuta `docker compose down -v`)*
