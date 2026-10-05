# Gestor de Stock - Práctico Django REST Framework

Proyecto desarrollado para el espacio curricular **Ingeniería de Software** del Instituto Tecnológico Río Cuarto (ITEC).
API REST para la gestión de productos y stock de un emprendimiento de pastas, construida con **Django**, **Django REST Framework (DRF)** y gestionada con **uv**.

---

## Características Principales y Arquitectura

* **ViewSets y Routers**:
  - `CategoriaViewSet`: hereda de `viewsets.ReadOnlyModelViewSet` para exponer operaciones de consulta pública (`list`, `retrieve`).
  - `ProductoViewSet`: hereda de `viewsets.ModelViewSet` implementando un CRUD completo, optimización ORM con `select_related('categoria')`, alternancia dinámica de serializers y acción personalizada `@action` para productos disponibles (`/api/productos/disponibles/`).
  - Enrutamiento automático con `DefaultRouter` en `src/productos/routers.py`.
* **Autenticación con SimpleJWT**:
  - Emisión de tokens de acceso (`access`) y refresco (`refresh`) mediante `/api/token/` y `/api/token/refresh/`.
  - Soporte de `SessionAuthentication` para interacción fluida desde la Browsable API de DRF (`/api-auth/`).
* **Seguridad y Permisos Granulares**:
  - `CategoriaViewSet`: acceso de solo lectura abierto (`AllowAny`).
  - `ProductoViewSet`: `get_permissions()` dinámico — consultas públicas (`AllowAny`), mutaciones protegidas (`IsAuthenticated`).

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

### 4. Crear un superusuario / usuario para pruebas de autenticación
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
* **API Root (Browsable API)**: `http://127.0.0.1:8000/api/`
* **Login de Sesión Browsable API**: `http://127.0.0.1:8000/api-auth/login/`
* **Admin de Django**: `http://127.0.0.1:8000/admin/`

---

## Endpoints Disponibles

### Autenticación (SimpleJWT)
| Método HTTP | Endpoint | Permisos | Descripción |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/token/` | Público | Obtiene par de tokens (`access` y `refresh`) enviando `username` y `password` |
| `POST` | `/api/token/refresh/` | Público | Renueva el token de acceso enviando `{"refresh": "<token>"}` |

### Categorías (`ReadOnlyModelViewSet`)
| Método HTTP | Endpoint | Permisos | Descripción |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/categorias/` | Público (`AllowAny`) | Lista todas las categorías |
| `GET` | `/api/categorias/<id>/` | Público (`AllowAny`) | Detalle de una categoría por ID |

### Productos (`ModelViewSet`)
| Método HTTP | Endpoint | Permisos | Descripción |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/productos/` | Público (`AllowAny`) | Lista productos con **categoría anidada** (`select_related`) |
| `POST` | `/api/productos/` | Autenticado (`IsAuthenticated`) | Crea un nuevo producto (pasando `categoria`: ID) |
| `GET` | `/api/productos/<id>/` | Público (`AllowAny`) | Detalle de un producto con **categoría anidada** |
| `PUT` | `/api/productos/<id>/` | Autenticado (`IsAuthenticated`) | Actualiza completamente un producto por ID |
| `PATCH` | `/api/productos/<id>/` | Autenticado (`IsAuthenticated`) | Actualiza parcialmente un producto por ID |
| `DELETE` | `/api/productos/<id>/` | Autenticado (`IsAuthenticated`) | Elimina un producto por ID |
| `GET` | `/api/productos/disponibles/`| Público (`AllowAny`) | Acción custom: lista solo productos con `disponible = true` |

---

## Guía de Pruebas Manuales (Postman / Bruno / ThunderClient / cURL)

### 1. Obtener Token JWT (POST)
* **URL**: `http://127.0.0.1:8000/api/token/`
* **Método**: `POST`
* **Body (JSON)**:
  ```json
  {
    "username": "tu_usuario",
    "password": "tu_password"
  }
  ```
* **Respuesta esperada**: Status `200 OK`
  ```json
  {
    "access": "eyJhbGciOi...",
    "refresh": "eyJhbGciOi..."
  }
  ```

---

### 2. Listar Categorías (GET - Público)
* **URL**: `http://127.0.0.1:8000/api/categorias/`
* **Método**: `GET`
* **Respuesta esperada**: Status `200 OK` con la lista de categorías.

---

### 3. Crear Producto sin Token (POST - Rechazado)
* **URL**: `http://127.0.0.1:8000/api/productos/`
* **Método**: `POST`
* **Body**: Datos de producto.
* **Respuesta esperada**: Status `401 Unauthorized`.

---

### 4. Crear Producto con Token (POST - Autorizado)
* **URL**: `http://127.0.0.1:8000/api/productos/`
* **Método**: `POST`
* **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <tu_access_token>`
* **Body (JSON)**:
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
* **Respuesta esperada**: Status `201 Created`.

---

### 5. Consultar Productos Disponibles (GET - Acción personalizada)
* **URL**: `http://127.0.0.1:8000/api/productos/disponibles/`
* **Método**: `GET`
* **Respuesta esperada**: Status `200 OK` con únicamente productos en stock y disponibles.

---

### 6. Probar validación de precio inválido (POST con precio <= 0)
* **URL**: `http://127.0.0.1:8000/api/productos/`
* **Método**: `POST`
* **Headers**: `Authorization: Bearer <tu_access_token>`
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
