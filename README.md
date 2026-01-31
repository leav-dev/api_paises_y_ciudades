# Countries API - Documentación del Contrato de API

## Descripción General

### ¿Qué hace la API?
Esta aplicación consume la **API de REST Countries** para obtener información detallada sobre países de todo el mundo. La aplicación actúa como un intermediario que simplifica el acceso a los datos geográficos, demográficos y culturales de los países.

### ¿Qué información devuelve?
- **Nombre del país** consultado (común y oficial)
- **Capital** del país
- **Población** total
- **Monedas** utilizadas con códigos y símbolos
- **Idiomas** oficiales hablados
- **Región y subregión** geográfica
- **Bandera** del país (URL de la imagen)
- **Códigos de país** (ISO 2 y 3 letras)

### ¿Para qué sirve?
- Consultar información básica de cualquier país del mundo
- Integrar datos geográficos en aplicaciones web o móviles
- Obtener información relevante para sistemas de localización
- Validar códigos de país y monedas en formularios

---

## Endpoints Utilizados

La aplicación utiliza los endpoints de la API de REST Countries:

---

### 1. Obtener Todos los Países

| Campo | Descripción |
|-------|-------------|
| **URL del endpoint** | `https://restcountries.com/v3.1/all` |
| **Método HTTP** | `GET` |
| **Documentación oficial** | [REST Countries API](https://restcountries.com/) |

#### Parámetros Opcionales

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `fields` | string | ❌ No | Campos específicos a retornar (ej: "name,capital,population") |

#### Ejemplo de Petición

```http
GET https://restcountries.com/v3.1/all?fields=name,capital,population,currencies
```

#### Ejemplo de Respuesta Exitosa (JSON)

```json
[
  {
    "name": {
      "common": "Colombia",
      "official": "Republic of Colombia"
    },
    "capital": ["Bogotá"],
    "population": 50882884,
    "currencies": {
      "COP": {
        "name": "Colombian peso",
        "symbol": "$"
      }
    }
  }
]
```

---

### 2. Buscar País por Nombre

| Campo | Descripción |
|-------|-------------|
| **URL del endpoint** | `https://restcountries.com/v3.1/name/{name}` |
| **Método HTTP** | `GET` |
| **Documentación oficial** | [REST Countries API](https://restcountries.com/) |

#### Parámetros Requeridos

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `name` | string | ✅ Sí | Nombre del país a buscar (ej: "Colombia", "Spain") |
| `fullText` | boolean | ❌ No | Búsqueda exacta (true) o parcial (false, por defecto) |

#### Ejemplo de Petición

```http
GET https://restcountries.com/v3.1/name/colombia
```

#### Ejemplo de Respuesta Exitosa (JSON)

```json
[
  {
    "name": {
      "common": "Colombia",
      "official": "Republic of Colombia",
      "nativeName": {
        "spa": {
          "official": "República de Colombia",
          "common": "Colombia"
        }
      }
    },
    "tld": [".co"],
    "cca2": "CO",
    "ccn3": "170",
    "cca3": "COL",
    "capital": ["Bogotá"],
    "region": "Americas",
    "subregion": "South America",
    "languages": {
      "spa": "Spanish"
    },
    "currencies": {
      "COP": {
        "name": "Colombian peso",
        "symbol": "$"
      }
    },
    "population": 50882884,
    "flags": {
      "png": "https://flagcdn.com/w320/co.png",
      "svg": "https://flagcdn.com/co.svg"
    }
  }
]
```

---

### 3. Buscar Países por Moneda

| Campo | Descripción |
|-------|-------------|
| **URL del endpoint** | `https://restcountries.com/v3.1/currency/{currency}` |
| **Método HTTP** | `GET` |
| **Documentación oficial** | [REST Countries API](https://restcountries.com/) |

#### Parámetros Requeridos

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `currency` | string | ✅ Sí | Código de moneda ISO (ej: "USD", "EUR", "COP") |

#### Ejemplo de Petición

```http
GET https://restcountries.com/v3.1/currency/usd
```

---

### 4. Buscar Países por Idioma

| Campo | Descripción |
|-------|-------------|
| **URL del endpoint** | `https://restcountries.com/v3.1/lang/{language}` |
| **Método HTTP** | `GET` |
| **Documentación oficial** | [REST Countries API](https://restcountries.com/) |

#### Parámetros Requeridos

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `language` | string | ✅ Sí | Código de idioma ISO (ej: "spa", "eng", "fra") |

#### Ejemplo de Petición

```http
GET https://restcountries.com/v3.1/lang/spa
```

---

## Manejo de Errores

### Códigos de Error Posibles

| Código HTTP | Significado | Causa Común |
|-------------|-------------|-------------|
| `400` | Bad Request | Parámetros inválidos o formato incorrecto |
| `404` | Not Found | País no encontrado con el nombre/código especificado |
| `429` | Too Many Requests | Límite de peticiones excedido (muy raro, la API es gratuita) |
| `500` | Internal Server Error | Error interno del servidor de REST Countries |
| `503` | Service Unavailable | Servicio temporalmente no disponible |

---

### Ejemplo de Respuesta de Error (País No Encontrado)

**Petición:**
```http
GET https://restcountries.com/v3.1/name/PaisInexistente
```

**Respuesta:**
```json
{
  "status": 404,
  "message": "Not Found"
}
```

**Explicación:** Cuando el país no existe, la API de REST Countries devuelve un error 404. Nuestra aplicación lo detecta y responde con:

```json
{
  "detail": "País 'PaisInexistente' no encontrado. Verifica el nombre e intenta de nuevo.",
  "error_code": "COUNTRY_NOT_FOUND",
  "timestamp": "2026-01-31T10:30:00Z"
}
```

---

### Ejemplo de Error de Parámetros Inválidos

**Petición:**
```http
GET https://restcountries.com/v3.1/currency/MONEDA_INVALIDA
```

**Respuesta:**
```json
{
  "status": 400,
  "message": "Bad Request"
}
```

**Explicación:** Cuando se proporciona un código de moneda inválido, la API devuelve un error 400.

---

## Endpoint de la Aplicación Local

### Obtener Información de un País

| Campo | Descripción |
|-------|-------------|
| **URL** | `http://localhost:8000/api/countries/{country}` |
| **Método HTTP** | `GET` |

#### Ejemplo de Petición

```http
GET http://localhost:8000/api/countries/colombia
```

#### Ejemplo de Respuesta Exitosa

```json
{
  "name": "Colombia",
  "official_name": "Republic of Colombia",
  "capital": "Bogotá",
  "population": 50882884,
  "region": "Americas",
  "subregion": "South America",
  "currencies": [
    {
      "code": "COP",
      "name": "Colombian peso",
      "symbol": "$"
    }
  ],
  "languages": ["Spanish"],
  "flag": "https://flagcdn.com/w320/co.png",
  "country_code": "CO"
}
```

#### Campos de Respuesta

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | string | Nombre común del país |
| `official_name` | string | Nombre oficial del país |
| `capital` | string | Capital principal del país |
| `population` | int | Población total |
| `region` | string | Región geográfica |
| `subregion` | string | Subregión específica |
| `currencies` | array | Lista de monedas con código, nombre y símbolo |
| `languages` | array | Lista de idiomas oficiales |
| `flag` | string | URL de la bandera del país |
| `country_code` | string | Código de país de 2 letras |

---

### Buscar Países por Moneda

| Campo | Descripción |
|-------|-------------|
| **URL** | `http://localhost:8000/api/countries/currency/{currency_code}` |
| **Método HTTP** | `GET` |

#### Ejemplo de Petición

```http
GET http://localhost:8000/api/countries/currency/usd
```

---

### Buscar Países por Idioma

| Campo | Descripción |
|-------|-------------|
| **URL** | `http://localhost:8000/api/countries/language/{language_code}` |
| **Método HTTP** | `GET` |

#### Ejemplo de Petición

```http
GET http://localhost:8000/api/countries/language/spa
```

---

## Configuración Requerida

### Variables de Entorno (.env)

```env
# REST Countries API - No requiere API Key
RESTCOUNTRIES_BASE_URL=https://restcountries.com/v3.1
RESTCOUNTRIES_TIMEOUT=10

# Configuración de la aplicación
APP_NAME=Countries API
APP_VERSION=1.0.0
```

### Ventajas de REST Countries API

1. **Gratuita**: No requiere registro ni API Key
2. **Sin límites**: No tiene restricciones de uso
3. **Completa**: Información detallada de todos los países
4. **Actualizada**: Datos mantenidos y actualizados regularmente
5. **Rápida**: Respuestas rápidas y confiables

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Python 3.7+**: Asegúrate de tener Python instalado
- **pip**: Gestor de paquetes de Python (viene incluido con Python)

### Paso 1: Clonar o Descargar el Proyecto

```bash
# Si tienes el proyecto en Git
git clone <url-del-repositorio>
cd countries-api

# O simplemente descarga los archivos del proyecto
```

### Paso 2: Crear un Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
# Instalar todas las dependencias desde requirements.txt
pip install -r requirements.txt

# O instalar manualmente:
pip install fastapi uvicorn python-dotenv httpx
```

### Paso 4: Configurar Variables de Entorno (Opcional)

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Crear archivo .env
touch .env  # En macOS/Linux
# En Windows: crear manualmente el archivo .env
```

Contenido del archivo `.env`:
```env
# Configuración de la API (opcional - tiene valores por defecto)
RESTCOUNTRIES_BASE_URL=https://restcountries.com/v3.1
RESTCOUNTRIES_TIMEOUT=10

# Información de la aplicación
APP_NAME=Countries API
APP_VERSION=1.0.0

# Configuración de logging
LOG_LEVEL=INFO

# Configuración de cache (opcional)
CACHE_TTL_SECONDS=3600
```

**Nota**: Este paso es opcional ya que la aplicación tiene valores por defecto para todas las configuraciones.

### Paso 5: Ejecutar la Aplicación

```bash
# Opción 1: Usando uvicorn directamente (recomendado para desarrollo)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Opción 2: Ejecutando el archivo main.py directamente
python main.py

# Opción 3: Para producción (sin --reload)
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Paso 6: Verificar que Funciona

Una vez que la aplicación esté ejecutándose, verás un mensaje similar a:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Ahora puedes acceder a:

- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

---

## 🧪 Probar la API

### Usando el Navegador

1. Ve a http://localhost:8000/docs
2. Expande el endpoint `/api/countries/{country}`
3. Haz clic en "Try it out"
4. Ingresa un país como "colombia" o "spain"
5. Haz clic en "Execute"

### Usando curl

```bash
# Obtener información de Colombia
curl http://localhost:8000/api/countries/colombia

# Obtener información de España
curl http://localhost:8000/api/countries/spain

# Verificar que la API está funcionando
curl http://localhost:8000/
```

### Usando Python requests

```python
import requests

# Obtener información de un país
response = requests.get("http://localhost:8000/api/countries/colombia")
data = response.json()

print(f"País: {data['name']}")
print(f"Capital: {data['capital']}")
print(f"Población: {data['population']:,}")
```

---

## 🛠️ Desarrollo

### Estructura del Proyecto

```
countries-api/
├── main.py                 # Punto de entrada de la aplicación
├── appsettings.py         # Configuración centralizada
├── requirements.txt       # Dependencias de Python
├── .env                   # Variables de entorno (opcional)
├── .gitignore            # Archivos a ignorar en Git
├── README.md             # Este archivo
├── controllers/          # Controladores (endpoints HTTP)
│   └── countrycontroller.py
├── services/             # Lógica de negocio
│   └── countryservices.py
├── clients/              # Clientes para APIs externas
│   └── countryClient.py
└── DTOs/                 # Modelos de datos
    └── countryDtos.py
```

### Comandos Útiles para Desarrollo

```bash
# Ejecutar con recarga automática (desarrollo)
uvicorn main:app --reload

# Ejecutar en un puerto específico
uvicorn main:app --reload --port 3000

# Ejecutar con logs detallados
uvicorn main:app --reload --log-level debug

# Verificar sintaxis de Python
python -m py_compile main.py

# Instalar nueva dependencia y actualizar requirements.txt
pip install nueva-libreria
pip freeze > requirements.txt
```

---

## 🐳 Docker (Opcional)

Si prefieres usar Docker, puedes crear un `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Y ejecutar:

```bash
# Construir imagen
docker build -t countries-api .

# Ejecutar contenedor
docker run -p 8000:8000 countries-api
```

---

## ❌ Solución de Problemas

### Error: "ModuleNotFoundError"

```bash
# Asegúrate de que el entorno virtual esté activado
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstala las dependencias
pip install -r requirements.txt
```

### Error: "Port already in use"

```bash
# Usa un puerto diferente
uvicorn main:app --reload --port 8001

# O mata el proceso que usa el puerto 8000
# En Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# En macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Error: "Connection refused" al consultar países

- Verifica tu conexión a internet
- La API de REST Countries podría estar temporalmente no disponible
- Intenta con un país diferente

### La aplicación no encuentra el archivo .env

- El archivo `.env` es opcional
- Asegúrate de que esté en la raíz del proyecto (mismo nivel que `main.py`)
- Verifica que no tenga extensión adicional (como `.env.txt`)

---

---

## Recursos Adicionales

- [Documentación oficial de REST Countries](https://restcountries.com/)
- [Repositorio en GitLab](https://gitlab.com/amatos/rest-countries)
- [Códigos de país ISO 3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)
- [Códigos de moneda ISO 4217](https://en.wikipedia.org/wiki/ISO_4217)
- [Códigos de idioma ISO 639](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

---

## 👤 Autor

- **Nombre:** Ing. Luis E. Albor Vega
- **Fecha:** Enero 2026

---

## Licencia

MIT License
