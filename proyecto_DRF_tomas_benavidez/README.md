# Gestor de Stock - Práctico Django REST Framework

Proyecto desarrollado para el espacio curricular **Ingeniería de Software** del Instituto Tecnológico Río Cuarto (ITEC).
API REST para la gestión de productos y stock de un emprendimiento de pastas, construida con **Django**, **Django REST Framework (DRF)** y gestionada con **uv**.

---

## Requisitos Previos

* **Python**: `>= 3.12`
* **uv**: Gestor de paquetes y entornos de Python ([Instalación de uv](https://docs.astral.sh/uv/getting-started/installation/)).

---

## Instalación y Configuración del Proyecto

### 1. Clonar el repositorio y entrar al directorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd proyecto_DRF_tomas_benavidez
```

### 2. Sincronizar dependencias y crear el entorno virtual
```bash
uv sync
```

### 3. Aplicar las migraciones a la base de datos
```bash
uv run python src/manage.py migrate
```

### 4. (Opcional) Crear un superusuario para el panel de administración
```bash
uv run python src/manage.py createsuperuser
```

---

## Cómo levantar el proyecto

Para iniciar el servidor de desarrollo de Django, ejecutá en tu terminal:

```bash
uv run python src/manage.py runserver
```

El servidor quedará escuchando en:
* **API REST / Browsable API**: `http://127.0.0.1:8000/api/productos/`
* **Admin de Django**: `http://127.0.0.1:8000/admin/`

---

## Endpoints Disponibles

| Método HTTP | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/productos/` | Lista todos los productos registrados |
| `POST` | `/api/productos/` | Crea un nuevo producto |
| `GET` | `/api/productos/<id>/` | Obtiene el detalle de un producto por ID |
| `PUT` | `/api/productos/<id>/` | Actualiza completamente un producto por ID |
| `PATCH` | `/api/productos/<id>/` | Actualiza parcialmente un producto por ID |
| `DELETE` | `/api/productos/<id>/` | Elimina un producto por ID |

---

## Guía de Pruebas Manuales (Postman / Bruno / ThunderClient)

Podés probar la API directamente desde la **Browsable API de DRF** en tu navegador o utilizando un cliente REST con los siguientes casos de prueba:

### 1. Crear un producto (POST)
* **URL**: `http://127.0.0.1:8000/api/productos/`
* **Método**: `POST`
* **Headers**: `Content-Type: application/json`
* **Body (JSON)**:
  ```json
  {
    "nombre": "Sorrentinos de Jamón y Queso",
    "descripcion": "Caja de 12 unidades artesanales",
    "categoria": "pasta_rellena",
    "precio": "8500.00",
    "stock": 25,
    "disponible": true
  }
  ```
* **Respuesta esperada**: Status `201 Created`
  ```json
  {
    "id": 1,
    "nombre": "Sorrentinos de Jamón y Queso",
    "descripcion": "Caja de 12 unidades artesanales",
    "categoria": "pasta_rellena",
    "precio": "8500.00",
    "stock": 25,
    "disponible": true,
    "creado_en": "2026-08-27T10:00:00Z",
    "actualizado_en": "2026-08-27T10:00:00Z"
  }
  ```

---

### 2. Listar todos los productos (GET)
* **URL**: `http://127.0.0.1:8000/api/productos/`
* **Método**: `GET`
* **Respuesta esperada**: Status `200 OK` con un array conteniendo los productos creados:
  ```json
  [
    {
      "id": 1,
      "nombre": "Sorrentinos de Jamón y Queso",
      "descripcion": "Caja de 12 unidades artesanales",
      "categoria": "pasta_rellena",
      "precio": "8500.00",
      "stock": 25,
      "disponible": true,
      "creado_en": "2026-08-27T10:00:00Z",
      "actualizado_en": "2026-08-27T10:00:00Z"
    }
  ]
  ```

---

### 3. Ver detalle de un producto (GET)
* **URL**: `http://127.0.0.1:8000/api/productos/1/`
* **Método**: `GET`
* **Respuesta esperada**: Status `200 OK` con la información del producto correspondiente.

---

### 4. Actualización parcial (PATCH)
* **URL**: `http://127.0.0.1:8000/api/productos/1/`
* **Método**: `PATCH`
* **Headers**: `Content-Type: application/json`
* **Body (JSON)**:
  ```json
  {
    "stock": 20,
    "precio": "9000.00"
  }
  ```
* **Respuesta esperada**: Status `200 OK` con los campos actualizados.

---

### 5. Probar validación de error (POST con precio inválido)
* **URL**: `http://127.0.0.1:8000/api/productos/`
* **Método**: `POST`
* **Headers**: `Content-Type: application/json`
* **Body (JSON)**:
  ```json
  {
    "nombre": "Fideos al Huevo",
    "precio": "-500.00",
    "stock": 10
  }
  ```
* **Respuesta esperada**: Status `400 Bad Request`
  ```json
  {
    "precio": [
      "El precio debe ser mayor a 0."
    ]
  }
  ```

---

### 6. Eliminar un producto (DELETE)
* **URL**: `http://127.0.0.1:8000/api/productos/1/`
* **Método**: `DELETE`
* **Respuesta esperada**: Status `204 No Content` (cuerpo de respuesta vacío).
