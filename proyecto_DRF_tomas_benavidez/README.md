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

### Categorías
| Método HTTP | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/categorias/` | Lista todas las categorías |
| `POST` | `/api/categorias/` | Crea una nueva categoría |
| `GET` | `/api/categorias/<id>/` | Detalle de una categoría por ID |
| `PUT` | `/api/categorias/<id>/` | Actualiza completamente una categoría |
| `PATCH` | `/api/categorias/<id>/` | Actualiza parcialmente una categoría |
| `DELETE` | `/api/categorias/<id>/` | Elimina una categoría (protegida si tiene productos) |

### Productos
| Método HTTP | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/productos/` | Lista productos con **categoría anidada** (`select_related`) |
| `POST` | `/api/productos/` | Crea un nuevo producto (pasando `categoria`: ID) |
| `GET` | `/api/productos/<id>/` | Detalle de un producto con **categoría anidada** |
| `PUT` | `/api/productos/<id>/` | Actualiza completamente un producto por ID |
| `PATCH` | `/api/productos/<id>/` | Actualiza parcialmente un producto por ID |
| `DELETE` | `/api/productos/<id>/` | Elimina un producto por ID |

---

## Guía de Pruebas Manuales (Postman / Bruno / ThunderClient / Browsable API)

Podés probar la API directamente desde la **Browsable API de DRF** en tu navegador o utilizando un cliente REST con el siguiente flujo de prueba:

### 1. Crear una Categoría (POST)
* **URL**: `http://127.0.0.1:8000/api/categorias/`
* **Método**: `POST`
* **Headers**: `Content-Type: application/json`
* **Body (JSON)**:
  ```json
  {
    "nombre": "Pastas Rellenas",
    "descripcion": "Pastas artesanales con relleno gourmet",
    "activa": true
  }
  ```
* **Respuesta esperada**: Status `201 Created`
  ```json
  {
    "id": 1,
    "nombre": "Pastas Rellenas",
    "descripcion": "Pastas artesanales con relleno gourmet",
    "activa": true,
    "creado_en": "2026-09-09T21:30:00Z"
  }
  ```

---

### 2. Listar Categorías (GET)
* **URL**: `http://127.0.0.1:8000/api/categorias/`
* **Método**: `GET`
* **Respuesta esperada**: Status `200 OK` con la lista de categorías.

---

### 3. Crear un Producto asociado a la Categoría (POST)
* **URL**: `http://127.0.0.1:8000/api/productos/`
* **Método**: `POST`
* **Headers**: `Content-Type: application/json`
* **Body (JSON)**: Enviamos únicamente la clave foránea (`categoria: 1`):
  ```json
  {
    "nombre": "Sorrentinos de Jamón y Queso",
    "descripcion": "Caja de 12 unidades artesanales",
    "categoria": 1,
    "precio": "8500.00",
    "stock": 25,
    "disponible": true
  }
  ```
* **Respuesta esperada**: Status `201 Created`

---

### 4. Listar Productos con Serializer Anidado (GET)
* **URL**: `http://127.0.0.1:8000/api/productos/`
* **Método**: `GET`
* **Respuesta esperada**: Status `200 OK` observando el objeto `categoria` completo anidado:
  ```json
  [
    {
      "id": 1,
      "nombre": "Sorrentinos de Jamón y Queso",
      "descripcion": "Caja de 12 unidades artesanales",
      "categoria": {
        "id": 1,
        "nombre": "Pastas Rellenas",
        "descripcion": "Pastas artesanales con relleno gourmet",
        "activa": true,
        "creado_en": "2026-09-09T21:30:00Z"
      },
      "precio": "8500.00",
      "stock": 25,
      "disponible": true,
      "creado_en": "2026-09-09T21:31:00Z",
      "actualizado_en": "2026-09-09T21:31:00Z"
    }
  ]
  ```

---

### 5. Ver detalle de un Producto con Serializer Anidado (GET)
* **URL**: `http://127.0.0.1:8000/api/productos/1/`
* **Método**: `GET`
* **Respuesta esperada**: Status `200 OK` con la categoría anidada.

---

### 6. Probar validación de precio inválido (POST con precio <= 0)
* **URL**: `http://127.0.0.1:8000/api/productos/`
* **Método**: `POST`
* **Body (JSON)**:
  ```json
  {
    "nombre": "Fideos al Huevo",
    "categoria": 1,
    "precio": "-100.00",
    "stock": 10
  }
  ```
* **Respuesta esperada**: Status `400 Bad Request` con mensaje `"El precio debe ser mayor a 0."`.

---

### 7. Probar protección de integridad referencial (DELETE Categoría en uso)
* **URL**: `http://127.0.0.1:8000/api/categorias/1/`
* **Método**: `DELETE`
* **Respuesta esperada**: Status `400 Bad Request`:
  ```json
  {
    "error": "No se puede eliminar la categoría porque tiene productos asociados."
  }
  ```

---

### 8. Eliminar un Producto (DELETE)
* **URL**: `http://127.0.0.1:8000/api/productos/1/`
* **Método**: `DELETE`
* **Respuesta esperada**: Status `204 No Content`. Una vez eliminado el producto, la categoría `1` sí podrá eliminarse.
