"""
=============================================================================
PUNTO DE ENTRADA DE LA APLICACIÓN FASTAPI
=============================================================================

Este es el archivo principal de la aplicación. Aquí se configura e inicializa
la instancia de FastAPI y se registran todos los routers (controladores).

FastAPI es un framework moderno y de alto rendimiento para construir APIs
con Python 3.7+ basado en estándares como OpenAPI y JSON Schema.

Características principales de FastAPI:
- Rápido: Rendimiento similar a NodeJS y Go
- Fácil: Diseñado para ser intuitivo
- Robusto: Código listo para producción
- Documentado: Genera docs automáticos (Swagger UI y ReDoc)

Para ejecutar la aplicación:
    uvicorn main:app --reload

Esto iniciará el servidor en http://localhost:8000

Documentación automática disponible en:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc

Autor: Ing. Eduardo Pimienta
Fecha: Enero 2026
=============================================================================
"""

# FastAPI es el framework principal para crear la API
# Importamos la clase FastAPI que será el núcleo de nuestra aplicación
from fastapi import FastAPI

# Importamos el router del controlador de países
# Los routers permiten organizar los endpoints en módulos separados
from controllers.countrycontroller import router as countries_router


# =============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# =============================================================================
# Creamos la instancia principal de FastAPI
# Esta instancia es el punto central que maneja todas las peticiones
app = FastAPI(
    title="Countries API",  # Título que aparece en la documentación
    description="""
    ## API de Países 🌍
    
    Esta API permite consultar información detallada sobre países de todo el mundo
    utilizando los servicios de REST Countries API.
    
    ### Funcionalidades:
    * Obtener información básica de países
    * Consultar población, capital y región
    * Ver monedas y idiomas oficiales
    * Buscar países por moneda o idioma
    * Obtener banderas de países
    
    ### Tecnologías utilizadas:
    * FastAPI - Framework web
    * httpx - Cliente HTTP asíncrono
    * Pydantic - Validación de datos
    * REST Countries API - Datos de países
    """,
    version="1.0.0",  # Versión de la API
    contact={
        "name": "Ing. Luis E. Albor",
        "email": "luis.e@example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)


# =============================================================================
# ENDPOINT RAÍZ (HOME)
# =============================================================================
@app.get(
    "/",
    summary="Página de inicio",
    description="Endpoint de bienvenida que confirma que la API está funcionando",
    tags=["General"]
)
def home():
    """
    Endpoint de bienvenida.
    
    Este endpoint sirve como verificación de que la API está funcionando
    correctamente. Es útil para health checks y monitoreo.
    
    Returns:
        dict: Mensaje de bienvenida
        
    Ejemplo de respuesta:
        {"message": "Welcome to the Countries API"}
    """
    return {
        "message": "Welcome to the Countries API",
        "docs": "Visita /docs para ver la documentación interactiva",
        "version": "1.0.0",
        "description": "API para consultar información de países del mundo"
    }


# =============================================================================
# REGISTRO DE ROUTERS
# =============================================================================
# Incluimos el router del controlador de países
# Esto registra todas las rutas definidas en weathercontroller.py
# 
# Después de esto, las siguientes rutas estarán disponibles:
# - GET /api/countries/{country} - Obtener información de un país
# - GET /api/countries/currency/{currency} - Buscar países por moneda
# - GET /api/countries/language/{language} - Buscar países por idioma
app.include_router(countries_router)


# =============================================================================
# NOTA SOBRE LA EJECUCIÓN
# =============================================================================
# Este bloque solo se ejecuta si corremos el archivo directamente
# En producción, usamos: uvicorn main:app --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    
    # Iniciamos el servidor de desarrollo
    # reload=True reinicia automáticamente cuando hay cambios en el código
    uvicorn.run(
        "main:app",  # Ruta al objeto app (archivo:variable)
        host="127.0.0.1",  # Solo accesible localmente
        port=8000,  # Puerto del servidor
        reload=True  # Reinicio automático en desarrollo
    )