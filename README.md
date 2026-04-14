# Beryllium Restaurante Backend

API REST de gestión de restaurante construida con Django 3.2 y Django REST Framework.

## Desarrollo Local

### 1. Configurar variables de entorno

Usar el archivo de ejemplo `.env.example` y completar las variables

### 2. Levantar la base de datos con Docker

```bash
docker-compose up -d
```

### 3. Realizar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

El servidor estará disponible en `http://localhost:8000/`

El panel de administración estará disponible en `http://localhost:8000/admin/`


## Solución de problemas comunes

Error al levantar Docker Compose con pyOpenSSL:
-> cambiar version a `pyOpenSSL==20.0.1`
